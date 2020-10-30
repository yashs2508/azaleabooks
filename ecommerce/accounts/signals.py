import stripe
import random 
import hashlib
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from .models import EmailConfirmed #have to import user stripe as well here
from django.db.models.signals import post_save
from django.core.mail import send_mail


# stripe.api_key = settings.STRIPE_SECRET_KEY


# def get_or_create_stripe(sender, user, *args, **kwargs): 
# 	# print(user.email)
# 	try:
# 		user.userstripe.stripe_id
# 	except UserStripe.DoesNotExist:
# 		customer = stripe.Customer.create(
#   			email = str(user.email)
# 	)
# 		new_user_stripe = UserStripe.objects.create(
# 				user = user,
# 				stripe_id =customer.id
# 		)
# 	except:
# 		pass

# user_logged_in.connect(get_or_create_stripe)


# def get_create_stripe(user):
# 	new_user_stripe,created = UserStripe.objects.get_or_create(user =user)
# 	if created:
# 		customer = stripe.Customer.create(
# 				email = str(user.email)
# 			)
# 		new_user_stripe.stripe_id = customer.id
# 		new_user_stripe.save()

def user_created(sender, instance, created, *args, **kwargs):
	user = instance
	# print(user.emailconfirmed.email_user())
	if created:
		# get_create_stripe(user)
		email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user = user)
		if email_is_created:
			short_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:7]
			base, domain = str(user.email).split("@")
			activation_key = hashlib.sha1(str(short_hash+base).encode('utf-8')).hexdigest()
			print(activation_key)
			email_confirmed.activation_key = activation_key
			email_confirmed.save()
			email_confirmed.activate_user_email()

post_save.connect(user_created, sender = settings.AUTH_USER_MODEL)

