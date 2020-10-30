from django.db import models
from products.models import Book, Variation
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
	# items = models.ManyToManyField(CartItem, blank=True)
	# products = models.ManyToManyField(Book, blank=True)
	total = models.DecimalField(max_digits= 100, decimal_places= 2, default= 0.00)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return "Cart id: %s" %(self.id)

class CartItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	cart = models.ForeignKey(Cart, default=1, on_delete=models.SET_DEFAULT)
	product = models.ForeignKey(Book, default=1, on_delete=models.SET_DEFAULT)
	variations = models.ManyToManyField(Variation, blank=True)
	quantity = models.IntegerField(default=1)
	notes = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		try:
			return str(self.cart.id)
		except:
			return self.product.title