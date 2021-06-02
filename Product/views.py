from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Product, Order, OrderItem
from Account.models import User, Customer, Profile, ShippingAddress
from Account.forms import EdithProfileForm
from .decorators import allowed_user
from .tasks import review_order_and_send_mail_task
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
import datetime

# Create your views here.
class Dashboard(TemplateView):
    template_name = 'Product/index.html'

    def get_context_data(self, **kwargs):
        queryset = Product.objects.all().exclude(quantity = 0).order_by('-quantity')
        context = {'queryset':queryset}
        return context

class ProductDetailView(TemplateView):
    template_name = 'Product/description.html'
        
    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get("pk")
        request = self.kwargs.get("request")
        product_details = Product.objects.get(id=id_)
        queryset = Product.objects.filter(category = str(product_details.category)).exclude(id = id_)[0:20]
        context = {'product_details': product_details, 'queryset':queryset}
        return context

def ShopByCategory(request):
    queryset_category = list(Product.objects.values_list('category', flat=True).distinct())
    queryset_brand = list(Product.objects.values_list('Brand', flat=True).distinct())
  
    brand_count=[]
    category_count = []
    
    for i in queryset_category:
        total = Product.objects.filter(category = str(i)).count()
        category_count.append([i,total])

    for i in queryset_brand:
        total = Product.objects.filter(Brand = str(i)).count()
        brand_count.append([i,total])

    queryset = Product.objects.all()

    if request.method == 'POST':
        category = request.POST.get('category')
        brand = request.POST.get('brand')
       
        if category != None and brand !=None:
            queryset = Product.objects.filter(category = str(category),Brand = str(brand))
            
        
        elif brand != None:
            queryset = Product.objects.filter(Brand = str(brand))
        
        elif category != None:
            queryset = Product.objects.filter(category = str(category))

    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context={'brand_count':brand_count,'category_count':category_count, 'queryset':queryset,'products':products}
    return render(request,'Product/category.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Customer'])
def cart(request):
    
    if request.user.is_authenticated:
      
        customer = Customer.objects.get(user = request.user)
       
        try:
            order = Order.objects.filter(customer = customer, complete = False)[0]
            items = order.orderitem_set.all()
        
        except:
            order = None
            items = []
      
    else:
        items = []
        order ={'get_car_total':0}
 
    context = {'items':items,'order':order}
    return render(request,'Product/cart.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
   
    customer = Customer.objects.get(user = request.user)
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer = customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
    

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
   
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    
    if action == 'delete':
        orderItem.delete()


    return JsonResponse('Item was added',safe = False)

@allowed_user(allowed_roles=['Customer'])
def checkout(request):
    
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(pk=user.id)
    try:
        address = ShippingAddress.objects.get(id = request.user.id)
        ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](instance = address)
    except:
        # address = None
        address,created = ShippingAddress.objects.get_or_create(id = request.user.id)
        ShippingAddress_form = EdithProfileForm.form_classes['addressedit']()
    User_form = EdithProfileForm.form_classes['useredit'](instance = user)
    Profile_form = EdithProfileForm.form_classes['profileedit'](instance = profile)
    # ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](instance = address)
    

    if request.method == 'POST':
        User_form = EdithProfileForm.form_classes['useredit'](request.POST,instance = user)
        Profile_form = EdithProfileForm.form_classes['profileedit'](request.POST,instance = profile)
        ShippingAddress_form = EdithProfileForm.form_classes['addressedit'](request.POST,instance = address)
        if User_form.is_valid() and Profile_form.is_valid() and ShippingAddress_form.is_valid():
            User_form.save()
            Profile_form.save()
            ShippingAddress_form.save()
            return redirect('checkout')

    if request.user.is_authenticated:
       
        customer = Customer.objects.get(user = request.user)
       
        try:
            order = Order.objects.filter(customer = customer, complete =False)[0]
            items = order.orderitem_set.all()
            for item in items:
                if item.quantity > item.product.quantity:
                    item.delete()
                    order.save()
            
            if order.get_cart_total == 0:
                messages.info(request,'Your Cart is Empty!')
                return redirect('cart')
        
        except:
            messages.info(request,'Your Cart is Empty!')
            return redirect('cart')
        

    else:
        items = []
        order ={'get_car_total':0}
    

    context={'User_form': User_form,'Profile_form':Profile_form,'ShippingAddress_form':ShippingAddress_form,'items':items,'order':order}     
    return render(request,'Product/checkout.html',context)


def confirmation(request):
    if request.user.is_authenticated:
        # print('request.user.is_customer: ',request.user.is_customer)
        if request.user.is_customer: 
        
            user = User.objects.get(id = request.user.id)
            profile = Profile.objects.get(pk=user.id) 
            address = ShippingAddress.objects.get(id = request.user.id)
            
            customer = Customer.objects.get(user = request.user)
        
            try:
                order = Order.objects.filter(customer = customer, complete =False)[0]
                items = order.orderitem_set.all()
                order.transaction_id = datetime.datetime.now().timestamp()
                order.complete = True
                order.save()
                data = list(items.values('id'))
                review_order_and_send_mail_task.delay(user.username,user.email,data,order.id)

            
            except:
                messages.info(request,'please create order')
                return redirect('Dashboard')
        
        else:
            messages.info(request,'please create order')
            return redirect('Dashboard')

           
      

    else:
        items = []
        order ={'get_cart_total':0}
    
 
    context = {'user':user, 'profile':profile, 'order':order, 'address':address ,'items':items}
    return render(request,'Product/confirmation.html',context)

def MyOrder(request):
    if request.user.is_authenticated:
        if request.user.is_customer: 

            customer = Customer.objects.get(user = request.user)
        
            try:
                prev_orders = Order.objects.filter(customer = customer, complete = True).order_by('date_orderd')[::-1]
            
                prev_order = {}
                for order_no in prev_orders:
                    Items = order_no.orderitem_set.all()
                    prev_order[order_no] = Items
            
            except:
                prev_order = None
            
        
        else:
            return redirect('login')
    else:
        prev_order = []
        messages.info(request,'Login required!')
        return redirect('login')
    # print(prev_order)
    context = {'prev_order':prev_order}
    return render(request,'Product/myorder.html',context)


def searchProduct(request):
   
    if request.method == 'POST':
        
        brand_name= request.POST.get('search-product')
        if brand_name:
            brand_name = brand_name.lower()
        
        queryset = Product.objects.filter(Brand = brand_name)
        context = {'brand_name':brand_name, 'queryset':queryset}
        return render(request,'Product/search.html',context)
    
    
    return render(request,'Account/login.html')