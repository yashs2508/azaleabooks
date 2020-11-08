from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from carts.models import Cart
from products.models import Book, Variation
from localflavor.in_.in_states import STATE_CHOICES

# Create your models here.



# STATUS_CHOICES = (
# 		("Started", "Started"),
# 		("Abandoned","Abandoned"),
# 		("Finished","Finished"),
# )

# class Order(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
# 	total = models.DecimalField(max_digits= 100, decimal_places= 2, default= 0.00)
# 	order_id = models.CharField(max_length=120, default="ABC", unique = True)
# 	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
# 	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")

# 	def __str__(self):
# 		return self.order_id

# class UserAddressManager(models.Manager):
# 	def get_billing_addresses(self, user):
# 		return super(UserAddressManager, self).filter(user= user)


# class UserAddress(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default=1)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
# 	First_Name= models.CharField(max_length = 120)
# 	Last_Name= models.CharField(max_length = 120) 
# 	address = models.CharField(max_length = 120)
# 	address_2 = models.CharField(max_length= 120, null= True, blank= True)
# 	city = models.CharField(max_length = 120)
# 	state = models.CharField(max_length = 120, choices = STATE_CHOICES)
# 	country = models.CharField(max_length = 120, default = "India")
# 	pincode = models.CharField(max_length = 120)
# 	phone = models.CharField(max_length = 120)
# 	shipping = models.BooleanField(default = True)
# 	billing = models.BooleanField(default = False)
# 	timestamp = models.DateTimeField(auto_now_add= True, auto_now= False)
# 	updated = models.DateTimeField(auto_now_add= True, auto_now= False)

# 	def __str__(self):
# 		return str(self.user.username)

# 	def get_address(self):
# 		return "%s %s, %s, %s, %s, %s, %s" %(self.First_Name, self.Last_Name ,self.address, self.city, self.state, self.country, self.pincode)

# 	objects = UserAddressManager()

# 	class Meta:
# 		ordering = ['-updated', '-timestamp']

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, editable=False, default="" )
    first_name = models.CharField(max_length=10, default="" )
    last_name = models.CharField(max_length=10, default="" )
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    address_2 = models.CharField(max_length= 120, null= True, blank= True)
    city = models.CharField( max_length=20, default="" )
    state = models.CharField(max_length = 120, choices = STATE_CHOICES, default="Uttar Pradesh")
    country = models.CharField(max_length=20, default="India")
    pincode = models.CharField(max_length = 120, default=262802)
    total = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True, null=True)
    update_at=models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    payment_method = forms.BooleanField(label='Payment Method: CASH ON DELIVERY')
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','address_2','phone','city','state','pincode','country']

class OrderProduct(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variation, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title