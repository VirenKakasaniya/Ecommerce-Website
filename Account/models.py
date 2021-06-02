from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver 
from django.db.models.signals import post_save 

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)

class ShippingAddress(models.Model):
    addressline_1 = models.CharField(max_length=150)
    addressline_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

class Profile(models.Model):
    user_id= models.ForeignKey(User, on_delete = models.CASCADE, primary_key=True)
    mobile_no = PhoneNumberField(null=True, blank=False, unique=True)
    Alt_mobile_no = PhoneNumberField(null=True, blank=False, unique=True)
    addresses = models.ManyToManyField(ShippingAddress)

@receiver(post_save, sender=User) #add this
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_id=instance)
        # print('profile created')