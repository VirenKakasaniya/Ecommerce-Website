from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('dashboard/', views.Dashboard, name='Dashboard'),
    path('Customer_register/',views.Customer_register.as_view(), name='Customer_register'),
    path('loginpage/', views.loginpage, name='login'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('profile/', views.profile, name='profile'),
    path('profile/EditProfile', views.EditProfile, name='EditProfile'),
    path('contact/', TemplateView.as_view(template_name='Account/contact.html'), name='Account_contact')
]