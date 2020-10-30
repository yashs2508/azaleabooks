import time
# import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
# from .models import UserAddress
# from accounts.forms import UserAddressForm
from carts.models import Cart, CartItem
from .models import Order, OrderForm, OrderProduct
from .utils import id_generator
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.template.loader import get_template
from django.core.mail import EmailMessage
# Create your views here.

# try:
# 	stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
# 	stripe_secret = settings.STRIPE_SECRET_KEY
# except Exception as e:
# 	print(str(e))
# 	raise NotImplementedError(str(e))

# stripe.api_key = stripe_secret


def orders(request):
	context = {}
	template = "orders/user.html"
	return render(request, template, context)


@login_required
def checkout(request):
	current_user = request.user
	# total = 0
	# for rs in shopcart:
	#     total += rs.product.Current_Price * rs.quantity
	try:
		the_id = request.session['cart_id']
		# shopcart = CartItem.objects.filter(user_id=the_id.id)
		# print(shopcart)
	except:
		the_id = None 
	if the_id:
		cart = Cart.objects.get(id=the_id)
		total=0.00
		for item in cart.cartitem_set.all():
			total = total + float(item.product.Listing_Price)

	if request.method == 'POST':  # if there is a post
		form = OrderForm(request.POST)
		#return HttpResponse(request.POST.items())
		if form.is_valid():
			# Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
			# ..............

			data = Order()
			data.first_name = form.cleaned_data['first_name'] #get product quantity from form
			data.last_name = form.cleaned_data['last_name']
			data.address = form.cleaned_data['address']
			data.city = form.cleaned_data['city']
			data.state = form.cleaned_data['state']
			data.country = form.cleaned_data['country']
			data.pincode = form.cleaned_data['pincode']
			data.phone = form.cleaned_data['phone']
			data.user_id = current_user.id
			data.total = total
			data.ip = request.META.get('REMOTE_ADDR')
			ordercode= get_random_string(10).upper() # random cod
			data.code =  ordercode
			data.save() #


			for rs in cart.cartitem_set.all():
				detail = OrderProduct()
				detail.order_id     = data.id # Order Id
				detail.product_id   = rs.product_id
				# detail.variant  = rs.variations.title
				detail.user_id      = current_user.id
				detail.quantity     = rs.quantity
				detail.price = rs.product.Listing_Price
				detail.amount       = data.total
				detail.save()
				# ***Reduce quantity of sold product from Amount of Product
				# if  rs.product.variations:
				#     product = Product.objects.get(id=rs.product_id)
				#     product.amount -= rs.quantity
				#     product.save()
				# else:
				#     print("Hello")
				#************ <> *****************

			del request.session['cart_id']
			del request.session['items_total']
			CartItem.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
			request.session['cart_items']=0
			messages.success(request, "Congratulations! Your Order has been placed. It will be delivered soon.")
			try:
				sendEmail(data.id)
				print("The order email has been sent.")
			except IOError as e:
				return e
			return HttpResponseRedirect(reverse("home"))
		else:
			messages.warning(request, form.errors)
			return HttpResponseRedirect(reverse("checkout"))
			return HttpResponse("Order !Done")

	form= OrderForm()
	# profile = UserProfile.objects.get(user_id=current_user.id)
	context = {
			   'total': total,
			   'form': form,
			   # 'profile': profile,
			   }
	return render(request, 'orders/checkout.html', context)



@login_required
def orderHistory(request):
  if request.user.is_authenticated:
	  user = request.user
	  order_details = Order.objects.filter(user_id= user.id)
	  print(order_details)
	  context = {
				  "order_details": order_details,
	  }
	  template = "orders/orders_list.html"
  return render(request, template, context) 


@login_required
def orderDetails(request, id):
	if request.user.is_authenticated:
		user = request.user
		order = Order.objects.get(user_id= user.id, id=id)
		orderitems = OrderProduct.objects.filter(order_id = id)
		context = {
					"order": order,
					"orderitems": orderitems,
		}
		template = "orders/orders_detail.html"
	return render(request, template, context)

def sendEmail(id):
	# user = request.user
	order = Order.objects.get(id=id)
	orderitems = OrderProduct.objects.filter(order_id = id)
	try:
		subject = "Azalea Books- New Order #{}".format(order.code)
		to = ['{}'.format(order.user.email)]
		print(to)
		from_email = settings.DEFAULT_FROM_EMAIL
		print(from_email)
		order_information={
		'order': order,
		'orderitems': orderitems
		}
		message = get_template('orders/email.html').render(order_information)
		print(message)
		msg = EmailMessage(subject,message, to=to, from_email=from_email)
		print(msg)
		msg.content_subtype = 'html'
		msg.send()
	except IOError as e:
		return e