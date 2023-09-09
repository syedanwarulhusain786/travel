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

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.utils.translation import gettext as _
import json





def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        mail = request.POST['inlineFormInputGroupUsername']
        password =request.POST['inlineFormInputGroupPassword']
        # mail=mail.lower()
        # password=password.lower()
        print(mail,password)
        user = authenticate(request, username=mail, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'index.html' )




#logout func. (called to logout and end session)
def logoutUser(request):
    logout(request)
    
    return redirect('index')