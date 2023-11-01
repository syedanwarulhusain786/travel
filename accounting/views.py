from django.shortcuts import render
from .models import *
# Create your views here.

from django.shortcuts import render
from django.shortcuts import render, redirect 
# Create your views here.
from django.urls import resolve
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from asyncio import exceptions
from django.conf import settings
from django.shortcuts import render,HttpResponse
# from httplib2 import Http,
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User#
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.utils.translation import gettext as _
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .filters import JournalEntryFilter  
from django.db.models import Q    
from datetime import datetime 
from accounting.currency import currency_symbols
def autocomplete(request):
    term = request.GET.get('term', '')
    # Implement your logic to fetch suggestions based on the input term
    suggestions = Ledger.objects.filter(ledger_name__icontains=term).values_list('ledger_name', flat=True)
    return JsonResponse(list(suggestions), safe=False)
def Account_chart(request):
    Category_list=Group.objects.all()
    # category_data = serializers.serialize('json', Category_list)
    accounts = Ledger.objects.all()

    return render(request, 'accountsCharts.html', context={
        'username':request.user,'IndividualAccount_list':accounts,'account_subcategory':Category_list
    })
def get_next_account_number(request):

    try:
        last_account = Ledger.objects.latest('ledger_number')
        next_account_number = last_account.ledger_number + 1
    except Ledger.DoesNotExist:
        next_account_number = 1001  # Initial account number

    return JsonResponse({'success': True, 'account_number': next_account_number})
def get_next_voucher_number(request):
    
    try:
        last_account = JournalEntries.objects.latest('voucherNo')
        next_account_number = 'JV-{}'.format(str(int(last_account.voucherNo) + 1))
    except JournalEntries.DoesNotExist:
        next_account_number = 'JV-'+str(100)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})    
def get_next_payment_voucher_number(request):
    
    try:
        last_account = Payment.objects.latest('voucherNo')
        next_account_number = 'Pay-{}'.format(str(int(last_account.voucherNo) + 1))
    except Payment.DoesNotExist:
        next_account_number = 'Pay-'+str(10000)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})    
def get_next_reciept_voucher_number(request):
    
    try:
        last_account = Receipt.objects.latest('voucherNo')
        next_account_number = 'Recieve-{}'.format(str(int(last_account.voucherNo) + 1))
        print(get_next_reciept_voucher_number)
    except Receipt.DoesNotExist:
        next_account_number = 'Recieve-'+str(10000)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})    
def get_next_sales_voucher_number(request):
    
    try:
        last_account = SalesReceipt.objects.latest('voucherNo')
        next_account_number = 'Sales-{}'.format(str(int(last_account.voucherNo) + 1))
    except SalesReceipt.DoesNotExist:
        next_account_number = 'Sales-'+str(10000)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})
def get_next_purchase_voucher_number(request):
    
    try:
        last_account = PurchaseReceipt.objects.latest('voucherNo')
        next_account_number = 'PR-{}'.format(str(int(last_account.voucherNo) + 1))
    except PurchaseReceipt.DoesNotExist:
        next_account_number = 'PR-'+str(10000)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})
def action(request):
    if request.method == "POST":
        data = request.POST  # Get the POST data
        action = data.get("action")
        
        # if action == "edit":
        #     # Handle edit action
        #     account_num = data.get("account_number")
        #     new_account_name = data.get("accountname")
        #     # Get the account to edit using the account number
        #     account_to_edit = IndividualAccount.objects.get(account_number=account_num)
        #     # Update the account name
        #     account_to_edit.account_name = new_account_name
        #     account_to_edit.save()
            
        #     return JsonResponse({'success': True, 'message': 'Account updated successfully'})

        if action == "delete":
            # Handle delete action
            account_number = data.get("account_number")

            # Delete the account using the account number
            try:
                account_to_delete = Ledger.objects.get(ledger_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except Ledger.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Group.objects.get(group_number=account_num)
            new_account = Ledger(group=category, ledger_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
def submit_journal(request):
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'voucher', '').split('-')[-1]
        invoice_no = data.get(f'invoice_no', '').split('-')[-1]
        invoice_date = data.get(f'invoice_date','')
        if not invoice_date:
            invoice_date=None
        print(invoice_date)
        
        narration = data.get(f'notes', '')  # Replace 'nar' with the actual key in your QueryDict
        
        # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            print(category_name)
            print(subcategory_name)
            
            debit = data.get(f'deb{i}', 0)
            if debit=='':
                debit=0.0# Default to 0 if not present or invalid
            credit = data.get(f'cre{i}', 0) 
            if credit =='':
                credit=0.0# Default to 0 if not present or invalid
            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            try:
                # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                category = Primary_Group.objects.get(primary_group_name=category_name)
                subcategory = Group.objects.get(group_name=subcategory_name.split('-')[-1])
                account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field

                # Create and save the JournalEntries instance
                entry = JournalEntries(
                    voucherNo=voucher_no,
                    narration=narration,
                    primary_group=category,
                    group=subcategory,
                    ledger=account,
                    debit=float(debit),
                    credit=float(credit),
                    invoice_no=invoice_no,
                    invoice_date=invoice_date
                      # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }
        print(entry_response)

        return JsonResponse({'success': True, 'message': entry_response})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
def journalEntries(request):
    context={}
    q=request.GET.get('q')
    from_date =request.GET.get('from')
    
    to_date =request.GET.get('to')
    
    context['username']=request.user
    # Parse date inputs (assuming they are in a specific format)
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date() if to_date else None
    except ValueError:
        from_date = None
        to_date = None

    if 'q' in request.GET:
        multiple_q = (
            Q(voucherNo__icontains=q) |
            Q(voucherCode__icontains=q) |
            Q(primary_group__primary_group_name__icontains=q) |
            Q(group__group_name__icontains=q) |
            Q(ledger__ledger_name__icontains=q)
        )

        # Apply date range filtering if both 'from_date' and 'to_date' are provided
        if from_date and to_date:
            filtered_entry = JournalEntryFilter(
                request.GET,
                queryset=JournalEntries.objects.filter(multiple_q, date__range=[from_date, to_date])
            )
        else:
            filtered_entry = JournalEntryFilter(request.GET, queryset=JournalEntries.objects.filter(multiple_q))
    else:
        # Apply date range filtering if both 'from_date' and 'to_date' are provided
        if from_date and to_date:
            filtered_entry = JournalEntryFilter(
                request.GET,
                queryset=JournalEntries.objects.filter(date__range=[from_date, to_date])
            )
        else:
            filtered_entry = JournalEntryFilter(request.GET, queryset=JournalEntries.objects.all())

    context['filtered_journal']=filtered_entry
    paginated_filtered_journal=Paginator(filtered_entry.qs,50)
    page_number=request.GET.get('page')
    journal_page_obj=paginated_filtered_journal.get_page(page_number)
    context['journal_page_obj']=journal_page_obj
    
    
    return render(request, 'journalEntries.html',context=context )  
def Journal_entry(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    accounts = Ledger.objects.all()
               

    return render(request, 'journalEntry.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,
    })
def Gernal_Ledger(request):
                
    accounts = Ledger.objects.all()           
    q=request.GET.get('q')
    lis=[]
    result={}
    cat=''
    subcat=''
    if 'q' in request.GET:
        ledgers=JournalEntries.objects.filter(account__account_name=q)
        cred=0
       
        deb=0
        bal=0
        for row in ledgers:
            led={}
      
            led['date']=row.date
            led['ledger']=row.ledger
            led['narration']=row.narration
            led['debit']=row.debit
            led['credit']=row.credit
            if row.debit==0.00:
                led['Balance']=-1*(row.credit)
            else:
                led['Balance']=row.debit
            cred=cred+row.credit
            deb=deb+row.debit
            bal=bal+led['Balance']
            lis.append(led)
        result={
          'deb_result':deb,
          'cred_result':cred,
          'bal_result':bal,
        
        }
        cat=row.primary_group.primary_group_name
        subcat=row.group.group_name
            

            
    return render(request, 'ledger.html', context={'heading':q,'cat':cat,'subcat':subcat,
        'username':request.user,'account_list':accounts,
        'ledger':lis,'result':result
    }) 
    
  

def paymentEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'paymentVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
def paymentList(request):
    print(request.user.username)    
               

    return render(request, 'paymentList.html', context={
        'username':request.user
    })

def submit_payment(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no', '')
        invoicedate = data.get(f'bankjournal_date', '')
        ttype = data.get(f'ttype', '')
        bankAmt_inWords = data.get(f'bankAmt_inWords', '')
        bankAmt_in_No =data.get(f'bankAmt_in_No', '')
        Banknotes = data.get(f'Banknotes', '')
        RecievedFrom = data.get(f'RecievedFrom', '')
        total = data.get(f'total', '')
        remark = data.get(f'cashTransaction_Id', '')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType', '')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType', '')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber', '')
                chequeDate = data.get(f'chequeDate', '')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency', '')
            
            bankDr = data.get(f'bankDr', '')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}', '')
                subcategory_name = data.get(f'sub{i}', '')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Payment(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    




def recieptEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'recieptVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
  
def submit_reciept(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no', '')
        invoicedate = data.get(f'bankjournal_date', '')
        ttype = data.get(f'ttype', '')
        bankAmt_inWords = data.get(f'bankAmt_inWords', '')
        bankAmt_in_No =data.get(f'bankAmt_in_No', '')
        Banknotes = data.get(f'Banknotes', '')
        RecievedFrom = data.get(f'RecievedFrom', '')
        total = data.get(f'total', '')
        remark = data.get(f'cashTransaction_Id', '')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType', '')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType', '')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber', '')
                chequeDate = data.get(f'chequeDate', '')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency', '')
            
            bankDr = data.get(f'bankDr', '')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}', '')
                subcategory_name = data.get(f'sub{i}', '')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Receipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
def recieptList(request):
    print(request.user.username)    
               

    return render(request, 'recieptList.html', context={
        'username':request.user
    })
    
    
def salesEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'sales_voucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'debit':debit,
    })  
def submitSales(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    voucher_no = data.get(f'voucher', '')
    invoicedate = data.get(f'invoice_date', '')
    debit_led = data.get(f'debit_led', '')
    total = data.get(f'd_total', '')
    
    deb_category = Primary_Group.objects.get(primary_group_name='INCOME')
    deb_subcategory = Group.objects.get(group_name='Sales')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            desc = data.get(f'ref{i}', 0)
            amt = data.get(f'amt{i}', 0)
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            print(account_num)
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                print(voucher_no)
                
                # Create and save the JournalEntries instance
                entry = SalesReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    decsription=desc,
                    amount=float(amt),
                    total=float(total),
                    
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
        
    
    
    
    
    
    
    

    
def salesList(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["Bank Account"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "Bank Account"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    print(currency)
    return render(request, 'recieptVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })  
  
  
def purchaseEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Purchase"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Purchase"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'purchaseVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'debit':debit,
        'cashs':cash
    })  
    
def purchaseList(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["Bank Account"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "Bank Account"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    print(currency)
    return render(request, 'purchaseVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
  
  
  
def submitpurchase(request):
    # Category_list=Primary_Group.objects.all()
    # Subcategory_list = Group.objects.all()
    # debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    # accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    # currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    bankDr = data.get(f'bankDr', '')
    
    voucher_no = data.get(f'invoice_no', '')
    invoicedate = data.get(f'invoice_date', '')
    debit_led = data.get(f'debit_led', '')
    total = data.get(f'd_total', '')
    
    deb_category = Primary_Group.objects.get(primary_group_name='EXPENSES')
    deb_subcategory = Group.objects.get(group_name='Purchase')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            desc = data.get(f'ref{i}', 0)
            amt = data.get(f'amt{i}', 0)
            bill_no = data.get(f'bill{i}', 0)
            
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            print(account_num)
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                print(voucher_no)
                
                # Create and save the JournalEntries instance
                entry = PurchaseReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    description=desc,
                    amount=float(amt),
                    total=float(total),
                    bill_no=bill_no
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
        
    
    
    
    
    
        
        
        
        
        
        

  
  
    
def Trial_Balance(request):
                
    accounts = Ledger.objects.values('ledger_name',)  
    led=[]
    res={}
    resdeb=0
    rescred=0
    resbal=0
    
    for account in accounts:        
        ledgers=JournalEntries.objects.filter(ledger__ledger_name=account['ledger_name'])
        print()
        cred=0
        deb=0
        bal=0
        for row in ledgers:
            
      
 
    
            cred=cred+row.credit
            deb=deb+row.debit
            bal=deb-cred
            
        le={'type':account['ledger_name'],
            'deb':deb,'cred':cred,'bal':bal
        }
        led.append(le)
        resdeb=resdeb+deb
        rescred=rescred+cred
        resbal=resbal+bal
    result={
        'deb_result':resdeb,
        'cred_result':rescred,
        'bal_result':resbal
    }        
    return render(request, 'trial_balance.html', context={
        'username':request.user,'account_list':accounts,
        'data':led,'result':result
    }) 
    
def Profit_Loss(request):
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
def Balance_sheet(request):
                
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
    
    
    
def maintain(request):
                
    print(request.user.username)    
               

    return render(request, 'maintain.html', context={
        'username':request.user
    })