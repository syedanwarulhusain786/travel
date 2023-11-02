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
    path('get_next_payment_voucher_number/', views.get_next_payment_voucher_number, name="get_next_payment_voucher_number"),
    path('get_next_reciept_voucher_number/', views.get_next_reciept_voucher_number, name="get_next_reciept_voucher_number"),
    
    path('get_next_purchase_voucher_number/', views.get_next_purchase_voucher_number, name="get_next_purchase_voucher_number"),
    path('get_next_sales_voucher_number/', views.get_next_sales_voucher_number, name="get_next_sales_voucher_number"),
    
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    
    path('action/', views.action, name="action"),
    path('submit_journal/', views.submit_journal, name="submit_journal"),
    path('journalEntries/', views.journalEntries, name="journalEntries"),
    path('maintain/', views.maintain, name="maintain"),
    
    
    path('paymentEntry/', views.paymentEntry, name="paymentEntry"),
    path('paymentList/', views.paymentList, name="paymentList"),
    path('submit_payment/', views.submit_payment, name="submit_payment"),
    
    path('recieptList/', views.recieptList, name="recieptList"),
    path('recieptEntry/', views.recieptEntry, name="recieptEntry"),
    path('submit_reciept/', views.submit_reciept, name="submit_reciept"),
    
    
    path('salesList/', views.salesList, name="salesList"),
    path('salesEntry/', views.salesEntry, name="salesEntry"),
    path('submitSales/', views.submitSales, name="submitSales"),
    
    path('purchaseList/', views.purchaseList, name="purchaseList"),
    path('purchaseEntry/', views.purchaseEntry, name="purchaseEntry"),
    path('submitpurchase/', views.submitpurchase, name="submitpurchase"),
    
    
    
    
    
    path('view_salesvoucher/<str:voucher_id>/', views.item_detail, name='item_detail'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    
]
