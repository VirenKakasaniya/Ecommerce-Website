from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.Adminloginpage, name='Adminloginpage'),
    path('Admin_register/', views.Admin_register.as_view(), name='Admin_register'),
    path('Adminlogoutpage/', views.Adminlogoutpage, name='Adminlogoutpage'),
    path('Adminprofile/', views.Adminprofile, name='Adminprofile'),
    path('Adminprofile/AdminEditProfile', views.AdminEditProfile, name='AdminEditProfile'),
    path('AdminDashboard/', views.AdminDashboard.as_view(), name='AdminDashboard'),
    path('AddProduct/', views.AddProduct, name='AddProduct'),
    path('productUpdate/<int:pk>/', views.productUpdate, name='productUpdate'),
    path('deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
    path('contact/', TemplateView.as_view(template_name='AdminSite/contact.html'), name='contact'),
    path('adminSearchProduct/', views.adminSearchProduct, name='adminSearchProduct'),
    path('Orders/', views.Orders, name='Orders'),

]