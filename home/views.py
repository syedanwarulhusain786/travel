from django.shortcuts import render

# Create your views here.

def home(request):    
    
            
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })

