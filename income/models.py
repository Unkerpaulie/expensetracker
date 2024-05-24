from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Source(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "income_source"
        ordering = ["name"]

    def __str__(self):
        return self.name    


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    income_date = models.DateField(default=now)
    description = models.CharField(max_length=200, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Income"
        ordering = ["-income_date"] # the - in front the field name denotes descending order

    def __str__(self):
        return f"{self.amount} earned from {self.category}"
    
