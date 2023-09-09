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
def autocomplete(request):
    term = request.GET.get('term', '')
    # Implement your logic to fetch suggestions based on the input term
    suggestions = IndividualAccount.objects.filter(accountname__icontains=term).values_list('accountname', flat=True)
    return JsonResponse(list(suggestions), safe=False)
def Account_chart(request):
    Category_list=Subcategory.objects.all()
    # category_data = serializers.serialize('json', Category_list)
    accounts = IndividualAccount.objects.all()
    print(accounts,'reload')           

    return render(request, 'accountsCharts.html', context={
        'username':request.user,'IndividualAccount_list':accounts,'account_subcategory':Category_list
    })
def get_next_account_number(request):

    try:
        last_account = IndividualAccount.objects.latest('account_number')
        next_account_number = last_account.account_number + 1
    except IndividualAccount.DoesNotExist:
        next_account_number = 1001  # Initial account number

    return JsonResponse({'success': True, 'account_number': next_account_number})
def get_next_voucher_number(request):
    
    try:
        last_account = JournalEntries.objects.latest('voucherNo')
        next_account_number = 'VN-{}'.format(str(int(last_account.voucherNo) + 1))
    except JournalEntries.DoesNotExist:
        next_account_number = 'VN-'+str(100)  # Initial account number

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
                account_to_delete = IndividualAccount.objects.get(account_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except IndividualAccount.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Subcategory.objects.get(subcategory_number=account_num)
            new_account = IndividualAccount(subcategory=category, account_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
def submit_journal(request):
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'voucher', '').split('-')[-1]
        narration = data.get(f'notes', '')  # Replace 'nar' with the actual key in your QueryDict
        
        # Loop through the data to create and save JournalEntries instances
        for i in range(1, 5):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            debit = data.get(f'deb{i}', 0)
            if debit=='':
                debit=0.0# Default to 0 if not present or invalid
            credit = data.get(f'cre{i}', 0) 
            if credit =='':
                credit=0.0# Default to 0 if not present or invalid
            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            try:
                # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                category = Category.objects.get(category_name=category_name)
                subcategory = Subcategory.objects.get(subcategory_name=subcategory_name.split('-')[-1])
                account = IndividualAccount.objects.get(account_number=account_num)  # Replace with the appropriate field
            
                # Create and save the JournalEntries instance
                entry = JournalEntries(
                    voucherNo=voucher_no,
                    narration=narration,
                    category=category,
                    subcategory=subcategory,
                    account=account,
                    debit=float(debit),
                    credit=float(credit),
                      # You can set comments as needed
                )
                entry.save()
            except Category.DoesNotExist:
                pass
            except Subcategory.DoesNotExist:
                pass
            except IndividualAccount.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.account.account_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
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
            Q(category__category_name__icontains=q) |
            Q(subcategory__subcategory_name__icontains=q) |
            Q(account__account_name__icontains=q)
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
                
    Category_list=Category.objects.all()
    Subcategory_list = Subcategory.objects.all()
    accounts = IndividualAccount.objects.all()
               

    return render(request, 'journalEntry.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,
    })
def Gernal_Ledger(request):
                
    accounts = IndividualAccount.objects.all()           
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
            led['account']=row.account
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
        cat=row.category.category_name
        subcat=row.subcategory.subcategory_name
            

            
    return render(request, 'ledger.html', context={'heading':q,'cat':cat,'subcat':subcat,
        'username':request.user,'account_list':accounts,
        'ledger':lis,'result':result
    }) 
    
  
  
  
  
  
  
  
  
  
  
  
    
def Trial_Balance(request):
                
    accounts = IndividualAccount.objects.values('account_name',)  
    led=[]
    res={}
    resdeb=0
    rescred=0
    resbal=0
    
    for account in accounts:        
        ledgers=JournalEntries.objects.filter(account__account_name=account['account_name'])
        print()
        cred=0
        deb=0
        bal=0
        for row in ledgers:
            
      
 
    
            cred=cred+row.credit
            deb=deb+row.debit
            bal=deb-cred
            
        le={'type':account['account_name'],
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