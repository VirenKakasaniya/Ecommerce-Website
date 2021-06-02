from django import forms
from django.contrib.auth.forms import UserCreationForm
from Product.models import Product
from Account.models import User, Employee
from django.db import transaction


class AdminSignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        # user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')
        # user.email = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user)
        employee.save()
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'