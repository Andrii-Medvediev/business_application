from django.db import models
from django.contrib.auth.models import User
from pages.models import AccountCategory, ExpenseCategory, IncomeCategory

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100, blank=False, null=False)
    account_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    date_and_time_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.account_name 
    
    class Meta:
        # unique_together = ('user', 'account_name')

        verbose_name = 'Рахунок'
        verbose_name_plural = 'Рахунки'
    
class ChangeType(models.Model):
    change_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    icon_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.change_name
    
    class Meta:
        verbose_name = 'Назва та іконка зміни в рахунку'
        verbose_name_plural = 'Назви та іконки змін в рахунках'


class AccountHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=True)
    change_type = models.ForeignKey(ChangeType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account} — {self.change_type.change_name}"
    
    class Meta:
        verbose_name = 'Зміна в рахунку'
        verbose_name_plural = 'Зміни в рахунках'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, related_name='from_account', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='to_account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.from_account.account_amount -= self.amount
        self.to_account.account_amount += self.amount
        self.from_account.save()
        self.to_account.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_account} -> {self.to_account} — {self.amount}"

    class Meta:
        verbose_name = 'Транзакція'
        verbose_name_plural = 'Транзакції'

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    tag = models.CharField(max_length=20, blank=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.account} - {self.amount} - {self.category}"

    class Meta:
        verbose_name = 'Витрата'
        verbose_name_plural = 'Витрати'

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    tag = models.CharField(max_length=20, blank=True, null=False)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.account} - {self.amount} - {self.category}"

    class Meta:
        verbose_name = 'Дохід'
        verbose_name_plural = 'Доходи'