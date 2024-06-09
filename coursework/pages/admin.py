from django.contrib import admin
from .models import Currency, AccountCategory, IncomeCategory, ExpenseCategory, Document

# Register your models here.
admin.site.register(Currency)
admin.site.register(AccountCategory)
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(Document)
