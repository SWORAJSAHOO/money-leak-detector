from django.db import models
class Income(models.Model): amount=models.IntegerField()
class Expense(models.Model): category=models.CharField(max_length=50); amount=models.IntegerField()
