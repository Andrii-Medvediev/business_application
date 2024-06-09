from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, ChangeType, AccountHistory, Transaction, Expense, Income
from .forms import AccountForm, TransactionForm, ExpenseForm, IncomeForm
from itertools import chain
from operator import attrgetter


@login_required
def accounts(request):
    user_accounts = Account.objects.filter(user=request.user, is_active=True).order_by('date_and_time_of_creation')
    total_balance = sum(account.account_amount for account in user_accounts)

    profile = request.user.profile
    currency_initials = profile.currency.initials if profile.currency else ''

    return render(request, 'finance/accounts.html', {'accounts': user_accounts, 'total_balance': total_balance, 
    'currency_initials': currency_initials})

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            # Запис у історію
            change_type = ChangeType.objects.get(change_name='Додавання рахунку')
            AccountHistory.objects.create(
                user=request.user,
                account=account,
                change_type=change_type,
                amount=account.account_amount
            )
            return redirect('finance:accounts')
    else:
        form = AccountForm(user=request.user)
    
    return render(request, 'finance/add_account.html', {'form': form})

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user, is_active=True)
    if request.method == 'POST':
        old_amount = account.account_amount
        form = AccountForm(request.POST, instance=account, user=request.user)
        if form.is_valid():
            account = form.save()

            # Обчислення різниці між старою та новою сумою
            difference = account.account_amount - old_amount

            # Запис у історію тільки якщо є різниця у сумі
            if difference != 0:
                change_type = ChangeType.objects.get(change_name='Редагування рахунку')
                AccountHistory.objects.create(
                    user=request.user,
                    account=account,
                    change_type=change_type,
                    amount=difference
                )
            return redirect('finance:accounts')
        
    else:
        form = AccountForm(instance=account, user=request.user)

    return render(request, 'finance/edit_account.html', {'form': form, 'account': account})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user, is_active=True)
    if request.method == 'POST':
        account_amount = account.account_amount

        account.is_active = False
        account.save()
        
        # Запис у історію
        change_type = ChangeType.objects.get(change_name='Видалення рахунку')
        AccountHistory.objects.create(
            user=request.user,
            account=account,
            change_type=change_type,
            amount=account_amount
        )
        return redirect('finance:accounts')
    return render(request, 'finance/delete_account.html', {'account': account})

@login_required
def expenses(request):
    user_expenses = Expense.objects.filter(user=request.user).order_by('-date_and_time')
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.account_amount for account in user_accounts)

    profile = request.user.profile
    currency_initials = profile.currency.initials if profile.currency else ''

    return render(request, 'finance/expenses.html', {'expenses': user_expenses, 'total_balance': total_balance, 'currency_initials': currency_initials})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('finance:expenses')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'finance/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    old_amount = expense.amount  # Збережемо стару суму витрат
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.account.account_amount += old_amount
            new_expense.account.save()
            new_expense.save()
            return redirect('finance:expenses')  # змініть на вашу URL-ім'я для списку витрат
    else:
        initial_data = {
            'date_and_time': expense.date_and_time.strftime('%Y-%m-%dT%H:%M')
        }
        form = ExpenseForm(instance=expense, initial=initial_data, user=request.user)
    return render(request, 'finance/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        account = expense.account
        account.account_amount += expense.amount
        account.save()
        expense.delete()
        return redirect('finance:expenses')  # змініть на вашу URL-ім'я для списку витрат
    return render(request, 'finance/delete_expense.html', {'expense': expense})

@login_required
def income(request):
    user_incomes = Income.objects.filter(user=request.user).order_by('-date_and_time')
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.account_amount for account in user_accounts)

    profile = request.user.profile
    currency_initials = profile.currency.initials if profile.currency else ''
    
    return render(request, 'finance/income.html', {'incomes': user_incomes, 'total_balance': total_balance, 'currency_initials': currency_initials})

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('finance:income')
    else:
        form = IncomeForm(user=request.user)
    return render(request, 'finance/add_income.html', {'form': form})

@login_required
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    old_amount = income.amount  # Збережемо стару суму доходу
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income, user=request.user)
        if form.is_valid():
            new_income = form.save(commit=False)
            difference = new_income.amount - old_amount
            new_income.account.account_amount += difference
            new_income.account.save()
            new_income.save()
            return redirect('finance:income')  # змініть на вашу URL-ім'я для списку доходів
    else:
        initial_data = {
            'date_and_time': income.date_and_time.strftime('%Y-%m-%dT%H:%M')
        }
        form = IncomeForm(instance=income, initial=initial_data, user=request.user)
    return render(request, 'finance/edit_income.html', {'form': form, 'income': income})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == "POST":
        account = income.account
        account.account_amount -= income.amount
        account.save()
        income.delete()
        return redirect('finance:income')  # змініть на вашу URL-ім'я для списку доходів
    return render(request, 'finance/delete_income.html', {'income': income})

@login_required
def transaction_history(request):
    history = AccountHistory.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)

    # Об'єднуємо записи з обох таблиць
    combined_history = sorted(
        chain(history, transactions),
        key=attrgetter('date_and_time'),
        reverse=True
    )

    profile = request.user.profile
    currency_initials = profile.currency.initials if profile.currency else ''
    
    return render(request, 'finance/transaction_history.html', {'history': combined_history, 'currency_initials': currency_initials})

@login_required
def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            return redirect('finance:accounts')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'finance/new_transaction.html', {'form': form})