from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from .models import User, Customer, Profile, ShippingAddress
from django.forms import ModelForm, fields, inlineformset_factory

# from account import models

class CustomerSignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        # user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()
        return user




class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
    
class ProfileEdithForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_no','Alt_mobile_no']

class ShippingAddressEdithForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields ='__all__'

class EdithProfileForm(forms.ModelForm):
    form_classes ={
        'useredit': UserEditForm,
        'profileedit': ProfileEdithForm,
        'addressedit': ShippingAddressEdithForm,
    }


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
    
    