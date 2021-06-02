from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.Dashboard.as_view(), name='Dashboard'),
    path('ProductDetailView/<int:pk>/', views.ProductDetailView.as_view(), name='ProductDetailView'),
    path('ShopByCategory/', views.ShopByCategory, name='ShopByCategory'),
    path('cart/', views.cart, name='cart'),
    path('update_Item/', views.updateItem, name='update_Item'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('MyOrder/', views.MyOrder, name='MyOrder'),
    path('contact/', TemplateView.as_view(template_name='Product/contact.html'), name='product_contact'),
    path('searchProduct/', views.searchProduct, name='searchProduct'),
]