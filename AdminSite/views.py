from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from Account.models import User,Profile, ShippingAddress
from Product.models import Product,Order
from .forms import AdminSignupForm, ProductForm
from Account.forms import EdithProfileForm
from Product.decorators import allowed_user
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@method_decorator(login_required(login_url='Adminloginpage'),name='dispatch')
@method_decorator(allowed_user(allowed_roles=['Admin']),name='dispatch')
class Admin_register(CreateView):
    model = User
    form_class = AdminSignupForm
    template_name = 'AdminSite/register.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('AdminDashboard')

def Adminloginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # return redirect('dashbord')
            return redirect('AdminDashboard')
        else:
            messages.info(request,'username or password incorrect')


    context={}
    return render(request,'AdminSite/login.html',context)

def Adminlogoutpage(request):
    logout(request)
    return redirect('Adminloginpage')


def Adminprofile(request):
    user = User.objects.get(id = request.user.id)
    try:
        profile = Profile.objects.get(pk=user.id)
        
    except:
        profile = Profile.objects.create(user_id = user)
        
    address = ShippingAddress.objects.get(id = request.user.id)
    User_form = EdithProfileForm.form_classes['useredit'](instance = user)
    Profile_form = EdithProfileForm.form_classes['profileedit'](instance = profile)
    ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](instance = address)

    context={'User_form': User_form,'Profile_form':Profile_form,'ShippingAddress_form':ShippingAddress_form}
    return render(request,'AdminSite/myprofile.html',context)


def AdminEditProfile(request):
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
        if User_form.is_valid():
            User_form.save()
            Profile_form.save()
            ShippingAddress_form.save()
            return redirect('AdminDashboard')

    context={'User_form': User_form,'Profile_form':Profile_form,'ShippingAddress_form':ShippingAddress_form}
    return render(request,'AdminSite/edit_profile.html',context)


@method_decorator(login_required(login_url='Adminloginpage'),name='dispatch')
@method_decorator(allowed_user(allowed_roles=['Admin']),name='dispatch')
class AdminDashboard(TemplateView):
    # template_name = 'dashboard.html'
    template_name = 'AdminSite/index1.html'

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        queryset = Product.objects.all()
        page = self.request.GET.get('page', 1)

        paginator = Paginator(queryset, 8)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {'products':products}
        return context
        

@login_required(login_url='Adminloginpage')
@allowed_user(allowed_roles=['Admin'])
def AddProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('AdminDashboard')
    
    context = {'form':form}
    return render(request,'AdminSite/Add_product.html',context)

def productUpdate(request,pk):
    product = Product.objects.get(id = pk)
    product_form = ProductForm(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(request.POST,request.FILES,instance = product)
       
        if product_form.is_valid():
            product_form.save()
            return redirect('AdminDashboard')

    context={'product_form': product_form, 'product':product}
    return render(request,'AdminSite/product_update.html',context)

def deleteProduct(request,pk):
    product = Product.objects.get(id = pk)
    if request.method=='POST':
        product.delete()
        return redirect('AdminDashboard')
    context = {'product':product}
    return render(request,'Adminsite/deleteproduct.html',context)

def adminSearchProduct(request):
   
    if request.method == 'POST':
        
        brand_name= request.POST.get('search-product')
        if brand_name:
            brand_name = brand_name.lower()
        
        queryset = Product.objects.filter(Brand = brand_name)
        context = {'brand_name':brand_name, 'queryset':queryset}
        return render(request,'Adminsite/search.html',context)
    
    
    return render(request,'Adminsite/login.html')


def Orders(request):
    queryset = Order.objects.all()
    orders = {}
    for order_no in queryset:
        Items = order_no.orderitem_set.all()
        orders[order_no] = Items
        

    context = {'orders':orders}
    return render(request,'AdminSite/orders.html',context)