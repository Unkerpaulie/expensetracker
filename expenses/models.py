from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name    


class Expense(models.Model):
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_date = models.DateField(default=now)
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="expenses", on_delete=models.CASCADE)

    @property
    def category_name(self):
        return self.category.name

    @property
    def expense_year(self):
        return self.expense_date.year

    @property
    def expense_month(self):
        return self.expense_date.month

    
    class Meta:
        ordering = ["-expense_date"] # the - in front the field name denotes descending order

    def __str__(self):
        return f"{self.amount} spent on {self.category}"
    
