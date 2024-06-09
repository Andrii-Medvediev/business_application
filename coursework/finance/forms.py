# finance/forms.py
from django import forms
from .models import Account, AccountCategory, Transaction, Income, Expense
from datetime import datetime

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'account_amount', 'category']
        widgets = {
            'account_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'accountName',
                'required': True,
            }),
            'account_amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'amount',
                'step': '0.01',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'accountCategory',
                'required': True,
            }),
        }
        labels = {
            'account_name': 'Назва рахунку',
            'account_amount': 'Кількість грошей',
            'category': 'Категорія рахунку',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AccountCategory.objects.all()

    def clean_account_name(self):
        account_name = self.cleaned_data.get('account_name')
        # Перевірка тільки для нових рахунків
        if not self.instance.pk:
            if Account.objects.filter(user=self.user, account_name=account_name, is_active=True).exists():
                raise forms.ValidationError('Рахунок з такою назвою вже існує.')
        return account_name


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['from_account', 'to_account', 'amount']
        widgets = {
            'from_account': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'to_account': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=self.user)
        self.fields['to_account'].queryset = Account.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get("from_account")
        to_account = cleaned_data.get("to_account")
        amount = cleaned_data.get("amount")

        if from_account == to_account:
            self.add_error('to_account', "Рахунки повинні бути різними")
        if amount is not None and amount <= 0:
            self.add_error('amount', "Сума повинна бути додатньою")
        if from_account and amount is not None and amount > from_account.account_amount:
            self.add_error('amount', "Недостатньо коштів")
        return cleaned_data
    

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['account', 'amount', 'category', 'date_and_time', 'tag', 'comment']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date_and_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=self.user)
        # Задаємо початкове значення для date_and_time, якщо воно не задане
        if self.instance and self.instance.pk and self.instance.date_and_time:
            self.fields['date_and_time'].initial = self.instance.date_and_time.strftime('%Y-%m-%dT%H:%M')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        account = self.cleaned_data.get('account')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Сума повинна бути більшою за нуль.")
        if round(amount, 2) != amount:
            raise forms.ValidationError("Сума повинна мати не більше двох знаків після коми.")
        if account and amount > account.account_amount:
            raise forms.ValidationError("Сума витрат не повинна бути більшою ніж кількість грошей на рахунку.")
        return amount

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        if not tag:
            raise forms.ValidationError("Це поле обов'язкове.")
        return tag

    def save(self, commit=True):
        expense = super().save(commit=False)
        if not expense.date_and_time:
            expense.date_and_time = datetime.now()
        expense.user = self.user
        expense.account.account_amount -= expense.amount
        expense.account.save()
        if commit:
            expense.save()
        return expense
    
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['account', 'amount', 'category', 'date_and_time', 'tag', 'comment']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date_and_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=self.user)
        # Задаємо початкове значення для date_and_time, якщо воно задане
        if self.instance and self.instance.pk and self.instance.date_and_time:
            self.fields['date_and_time'].initial = self.instance.date_and_time.strftime('%Y-%m-%dT%H:%M')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Сума повинна бути більшою за нуль.")
        if round(amount, 2) != amount:
            raise forms.ValidationError("Сума повинна мати не більше двох знаків після коми.")
        return amount

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        if not tag:
            raise forms.ValidationError("Це поле обов'язкове.")
        return tag

    def save(self, commit=True):
        income = super().save(commit=False)
        if not income.date_and_time:
            income.date_and_time = datetime.now()
        income.user = self.user
        income.account.account_amount += income.amount  # Додати суму до рахунку
        income.account.save()
        if commit:
            income.save()
        return income