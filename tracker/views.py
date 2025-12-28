from django.shortcuts import render, redirect
from .models import Income, Expense


def input_view(request):
    if request.method == "POST":

        income = request.POST.get("income")

        #  reset case
        if not income:
            Income.objects.all().delete()
            Expense.objects.all().delete()
            return redirect("home")

        # save income
        Income.objects.create(amount=int(income))
        Expense.objects.all().delete()

        categories = request.POST.getlist("category")
        amounts = request.POST.getlist("amount")

        for c, a in zip(categories, amounts):
            try:
                amount = int(a)
                if amount > 0:
                    Expense.objects.create(
                        category=c,
                        amount=amount
                    )
            except (ValueError, TypeError):
                continue

        return redirect("result")

    return render(request, "tracker/input.html")


def result_view(request):
    income_obj = Income.objects.last()
    expenses = Expense.objects.all()

    # safety check
    if not income_obj or not expenses.exists():
        return redirect("home")

    income = income_obj.amount

    total_spent = sum(e.amount for e in expenses)
    remaining = income - total_spent

    biggest = max(expenses, key=lambda x: x.amount)
    percent = round((biggest.amount / income) * 100, 1)

    labels = [e.category for e in expenses]
    values = [e.amount for e in expenses]

    top_expenses = sorted(
        expenses,
        key=lambda x: x.amount,
        reverse=True
    )[:3]

    return render(request, "tracker/result.html", {
        "income": income,
        "total_spent": total_spent,
        "remaining": remaining,
        "biggest": biggest,
        "percent": percent,
        "save": max(biggest.amount - 3000, 0),
        "labels": labels,
        "values": values,
        "top_expenses": top_expenses
    })
