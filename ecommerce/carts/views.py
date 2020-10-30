from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import Cart, CartItem
from products.models import Book, Variation

# Create your views here.


def view(request):
	try:
		the_id = request.session['cart_id']
	except:
		the_id = None 
	if the_id:
		cart = Cart.objects.get(id=the_id)
		new_total=0.00
		for item in cart.cartitem_set.all():
			new_total = new_total + float(item.product.Listing_Price)
		request.session['items_total'] =  cart.cartitem_set.count()
		cart.total = new_total
		cart.save()
		context = {"cart":cart}
	else:
		empty_message ="Your Cart is empty, please keep shopping!"
		context = {"empty": True,"empty_message":empty_message}
	
	template = 'cart/view.html'
	return render(request, template, context)


def remove_from_cart(request,id):
	try:
		the_id = request.session['cart_id']
		cart= Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse("view"))

	cartitem= CartItem.objects.get(id = id)
	cartitem.delete()
	return HttpResponseRedirect(reverse("view"))




def add_to_cart(request,id):
	request.session.set_expiry(1200000)
	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id= new_cart.id
	
	cart= Cart.objects.get(id=the_id)

	try:
		product= Book.objects.get(id=id)
	except Book.DoesNotExist:
		pass
	except:
		pass
	
	product_var= [] #product_variation

	if request.method == "POST":
		print(request.POST)
		# for item in request.POST:
		# 	print(item)
		key = 'action'
		val = request.POST[key]
		print(key,val)
		try:
			v = Variation.objects.get(product=product,cat__iexact=key, title__iexact=val)
			print(v)
			product_var.append(v)
		except:
			pass
		cart_item = CartItem.objects.create(cart=cart, product=product)
		if len(product_var) > 0:
			cart_item.variations.add(*product_var)
		cart_item.save()
		return HttpResponseRedirect(reverse("view"))

	return HttpResponseRedirect(reverse("view"))