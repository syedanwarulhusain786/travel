from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.utils.translation import gettext as _

urlpatterns = [
    

    
    path('accountsChart/', views.Account_chart, name="accountsChart"),
    
    path('journalEntry/', views.Journal_entry, name="journalEntry"),
    
    path('generalLedger/', views.Gernal_Ledger, name="generalLedger"),
    
    path('trialBalance/', views.Trial_Balance, name="trialBalance"),
    
    path('profitAndLoss/', views.Profit_Loss, name="profitAndLoss"),
    
    path('balanceSheet/', views.Balance_sheet, name="balanceSheet"),
    path('get_next_account_number/', views.get_next_account_number, name="get_next_account_number"),
    path('get_next_voucher_number/', views.get_next_voucher_number, name="get_next_voucher_number"),
    
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    
    path('action/', views.action, name="action"),
    path('submit_journal/', views.submit_journal, name="submit_journal"),
    path('journalEntries/', views.journalEntries, name="journalEntries"),
    path('maintain/', views.maintain, name="maintain"),
    
    
    path('paymentEntry/', views.paymentEntry, name="paymentEntry"),
    
    path('paymentList/', views.paymentList, name="paymentList"),
    
    path('recieptList/', views.recieptList, name="recieptList"),
    
    path('recieptEntry/', views.recieptEntry, name="recieptEntry"),
    
    
    
    
    
    
    
    
]
