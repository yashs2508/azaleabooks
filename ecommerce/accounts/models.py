
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
# from orders.models import UserAddress
# Create your models here.

# class UserDefaultAddress(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
# 	shipping = models.ForeignKey(UserAddress, on_delete = models.CASCADE, null= True, blank= True,\
# 								 related_name="user_address_shipping_default")
# 	billing = models.ForeignKey(UserAddress, on_delete = models.CASCADE, null= True, blank= True,\
# 								 related_name="user_address_billing_default")

# 	def __str__(self):
# 		return str(self.user.username)


# class UserAddressManager(models.Manager):
# 	def get_billing_addresses(self, user):
# 		return super(UserAddressManager, self).filter(user= user)


# class UserAddress(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
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


# class UserStripe(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
# 	stripe_id = models.CharField(max_length = 120, null = True, blank = True)

# 	def __str__(self):
# 		return str(self.stripe_id)


# "id": "cus_HvCoCk8JCH0EaV"
#cus_HvCoCk8JCH0EaV

class EmailConfirmed(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	activation_key = models.CharField(max_length = 200)
	confirmed = models.BooleanField(default = False)

	def __str__(self):
		return str(self.confirmed)

	def activate_user_email(self):
		activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view", args= [self.activation_key]))
		context = {
			"activation_key": self.activation_key,
			"activation_url": activation_url,
			"user" : self.user.username
		}
		message = render_to_string("accounts/activation_message.txt", context)
		subject = "Email Confirmation"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email = None, **kwargs):
		send_mail(subject, message, from_email, [self.user.email], kwargs)



