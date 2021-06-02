from django.db import models
from Account.models import Customer
# Create your models here.
class Product(models.Model):
    currencies = [
    ('$', "US Dollars ($)"),
    ('₹', "Indian Rupees (₹)") ,
    ]

    category = models.CharField(max_length=40 )
    name = models.CharField(max_length=40)
    description = models.TextField()
    currency = models.CharField(max_length=5, choices=currencies, default="$")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Brand = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0,null=True)
    image = models.ImageField(upload_to = 'images/')

    def save(self, *args, **kwargs):
        self.category = self.category.lower()
        self.name = self.name.lower()
        self.Brand = self.Brand.lower()
        return super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=10,null=True,default='Processing Order') 

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,null=True,default='Processing Item') 

    @property
    def get_total(self):
        if self.quantity > self.product.quantity:
            total = 0
        else:
            total = self.product.price * self.quantity
        return total

    @property
    def check_product_quantity(self):
        if self.quantity <= self.product.quantity:
            return True
        return False

    @property
    def update_product_quantity(self):
        if self.quantity <= self.product.quantity:
            self.product.quantity = self.product.quantity - self.quantity
            self.product.quantity = max(0,self.product.quantity)
            self.product.save()
            return 
          