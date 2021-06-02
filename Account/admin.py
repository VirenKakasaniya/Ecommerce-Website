from django.contrib import admin
from .models import User, Customer, Employee, ShippingAddress, Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_customer', 'is_admin']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Profile)