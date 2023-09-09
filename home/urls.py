from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.utils.translation import gettext as _

urlpatterns = [
    # # path('forgot/', views.forgot, name="forgot"),
    # path('signup/', views.signup, name="signup"),
    # path('partner_signup/', views.partner_signup, name="partner_signup"),
    
    # path('signin/', views.signin, name="signin"),
    # path('signup/<str:referral_code>/', views.signup, name='signup'),


    # path('', views.index, name="index"),
    # path('about-us/', views.about, name="about"), 

    # path('price/', views.price, name="price"), 

    # path('services/', views.services, name="services"), 

    # path('contact/', views.contact, name="contact"), 
    # path('home/', views.home, name="home"), 


    path('home/', views.home, name="home"),
	# path('index/', views.index, name="index"),  
    # path('activate_user/<uidb64>/<token>', views.activate_user, name="activate"),
    # # path('auth', views.activate_user, name="activate"),

    # #   PassWord Reset Urls 
    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='reset_password'),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    # path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),name='password_reset_confirm'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),


    # PassWord Reset Urls Finished

    
]
