from django.shortcuts import render,redirect
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView
from .models import User, Profile, ShippingAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerSignupForm, EdithProfileForm
# Create your views here.



class Customer_register(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = 'Account/register.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_customer:
                login(request,user)
                return redirect('Dashboard')
            
            else:
                messages.info(request,"You do not have customer account, Please register it")
                
        else:
            messages.info(request,'username or password incorrect')


    context={}
    return render(request,'Account/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    user = User.objects.get(id = request.user.id)
    profile,created = Profile.objects.get_or_create(pk=user.id)
    address,created = ShippingAddress.objects.get_or_create(id = request.user.id)

    User_form = EdithProfileForm.form_classes['useredit'](instance = user)
    Profile_form = EdithProfileForm.form_classes['profileedit'](instance = profile)
    ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](instance = address)

    context={'User_form': User_form,'Profile_form':Profile_form,'ShippingAddress_form':ShippingAddress_form}
    return render(request,'Account/myprofile.html',context)

@login_required(login_url='login')
def EditProfile(request):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(pk=user.id)
    address = ShippingAddress.objects.get(id = request.user.id)

    User_form = EdithProfileForm.form_classes['useredit'](instance = user)
    Profile_form = EdithProfileForm.form_classes['profileedit'](instance = profile)
    ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](instance = address)

    if request.method == 'POST':
        User_form = EdithProfileForm.form_classes['useredit'](request.POST,instance = user)
        Profile_form = EdithProfileForm.form_classes['profileedit'](request.POST,instance = profile)
        ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](request.POST,instance = address)
        if User_form.is_valid() and Profile_form.is_valid() and ShippingAddress_form.is_valid():
            User_form.save()
            Profile_form.save()
            ShippingAddress_form.save()

            return redirect('profile')
    context={'User_form': User_form,'Profile_form':Profile_form,'ShippingAddress_form':ShippingAddress_form}
    return render(request,'Account/edit_profile.html',context)