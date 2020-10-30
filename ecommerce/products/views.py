from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Book, Category, About, rentalsFAQ
from math import ceil 
from django.db.models import Q
from accounts.forms import ContactForm
from django.core.mail import EmailMessage

def home(request):
	# category = Category.objects.all()
	product_top = Book.objects.all().order_by('id')[:6]
	product_bottom = Book.objects.all().order_by('-id')[:6]
	product_middle = Book.objects.all().order_by('?')[:6]
	template = 'products/home.html'
	context = {'product_top':product_top, 'product_bottom':product_bottom, 'product_middle': product_middle,}
	return render(request,template, context)

def search(request):
	try:
		q = request.GET.get('field-keywords')
	except :
		q = None
	if q:
		book= Book.objects.filter(Q(title__icontains=q) | Q(Author__icontains=q) | Q(description__icontains=q))
		context = {'query':q, 'book':book}
		template='products/search.html'
	else:
		context={}
		template='products/home.html'
	return render(request, template, context)


def buy(request):
	products = Book.objects.all()
	template = 'products/buy.html'
	context = {
			'products': products,
	}
	return render(request, template, context)

def rentals(request):
	products = Book.objects.all().order_by('-id')
	template = 'products/rentals.html'
	context = {
			'products': products,
	}
	return render(request, template, context)

def about(request):
	about = About.objects.get()
	template= "products/about.html"
	context = {
			'about': about,
	}
	return render(request, template, context)

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data.get('subject')
			from_email = form.cleaned_data.get('Email')
			message = form.cleaned_data.get('message')
			name = form.cleaned_data.get('name')

			message_format = "{0} has sent you a new message:\n\n{1}".format(name, message)
			msg = EmailMessage(
				subject,
				message, 
				to=['help.azaleabooks@gmail.com'], 
				from_email=from_email
				)

			msg.send()
			messages.success(request, "Congratulations! Your Order has been placed. It will be delivered soon.")
			return HttpResponseRedirect(reverse("home"))
	else:	
		form = ContactForm() 
	
	template = 'products/contact.html'
	context = {
		'form': form 
	}
	return render(request, template, context)

def productview(request,id):
	try:
		book =  Book.objects.get(id=id)
		print(book)
		context = {'book':book}
		template = 'products/productview.html'
		return render(request, template, context)
	except:
		raise Http404


def rentalFAQ(request):
	faq = rentalsFAQ.objects.filter(status="True").order_by("prioritynumber")
	
	context = {
		'faq': faq,
	}
	template = "products/rentalsfaq.html"
	
	return render(request, template, context)
