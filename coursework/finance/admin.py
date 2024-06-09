from django.contrib import admin
from .models import Account, ChangeType, AccountHistory, Transaction, Expense, Income

admin.site.register(Account)
admin.site.register(ChangeType)
admin.site.register(AccountHistory)
admin.site.register(Transaction)
admin.site.register(Expense)
admin.site.register(Income)