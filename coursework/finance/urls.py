from django.urls import path
from . import views 

app_name = 'finance'

urlpatterns = [
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/<int:account_id>/', views.edit_account, name='edit_account'),
    path('accounts/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('expenses/', views.expenses, name='expenses'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('income/', views.income, name='income'),
    path('income/add/', views.add_income, name='add_income'),
    path('income/<int:income_id>/', views.edit_income, name='edit_income'),
    path('income/<int:income_id>/delete/', views.delete_income, name='delete_income'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('new_transaction/', views.new_transaction, name='new_transaction')
]