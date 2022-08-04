from django.db import models


class AccountData(models.Model):
    user = models.CharField(max_length=50)
    transaction_date = models.DateTimeField()
    transaction_balance = models.IntegerField()
    transaction_detail = models.CharField(max_length=70)
    transaction_memo = models.CharField(max_length=70, blank=True, null=True)
