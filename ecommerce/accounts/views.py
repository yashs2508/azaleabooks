import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import EmailConfirmed
# from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def logout_view(request):
	logout(request)
	messages.warning(request, "Successfully Logged Out! Feel free to Log In again.", extra_tags='email')
	return HttpResponseRedirect('%s'%(reverse('auth_login')))


def login_view(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username= username, password= password)
		login(request, user)
		messages.success(request, "Successfully Logged In! Welcome Back.")
		return HttpResponseRedirect(reverse('home'))
		# user.emailconfirmed.activate_user_email()
	# if request.method == 'POST':
	# 	form = AuthenticationForm(request.POST)
	# 	print(form)
	# 	if form.is_valid():
	# 		username = request.POST['username']
	# 		password = request.POST['password']
	# 		user = authenticate(username = username, password = password)
	# 		if user is not None:
	# 			login(request, user)
	# 			return HttpResponseRedirect(reverse('home'))
	# 		else:
	# 			return HttpResponseRedirect(reverse('view'))
	# else:
	# 	form = AuthenticationForm()

	context = {
		"form": form
	}
	return render(request, "form.html", context)


def registration_view(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		new_user = form.save(commit=False)
		# new_user.first_name = "Yash"
		new_user.save()
		messages.success(request, "Successfully Registered! Please Check your Email now for Confirmation.")
		return HttpResponseRedirect(reverse('home')) 
		# username = form.cleaned_data['username']
		# password = form.cleaned_data['password']
		# user = authenticate(username= username, password= password)
		# login(request, user)

	context = {
		"form": form
	}
	return render(request, "accounts/signup.html", context)
 
SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
	if SHA1_RE.search(activation_key):
		print("activaiton key is real")
		try:
			instance = EmailConfirmed.objects.get(activation_key = activation_key)
		except EmailConfirmed.DoesNotExist:
			instance = None
			messages.success(request, "There was an Error with your request.")
			return HttpResponseRedirect(reverse('home')) 
		if instance is not None and not instance.confirmed:
			page_message = "Confirmation Successful, Welcome!"
			instance.confirmed = True
			instance.activation_key = "Confirmed"
			instance.save()
			messages.success(request, "Successfully Confirmed!Please Login.")
		elif instance is not None and instance.confirmed:
			page_message = "Already Confirmed!"
			messages.success(request, "Already Confirmed!")
		else:
			page_message = ""

		context = {"page_message": page_message}
		return render(request, "accounts/activation_complete.html", context)
	else:
		raise Http404


# def add_user_address(request):
# 	print(request.GET)
# 	try:
# 		next_page = request.GET.get("next")
# 	except:
# 		next_page = None
# 	if request.method == "POST":
# 		form = UserAddressForm(request.POST)
# 		if form.is_valid():
# 			new_address = form.save()
# 			new_address.user = request.user
# 			new_address.save()
# 			is_default = form.cleaned_data["default"]
# 			if is_default:
# 				default_address, created = UserDefaultAddress.objects.get_or_create(user= request.user)
# 				default_address.shipping = new_address
# 				default_address.save()
# 			if next_page is not None:
# 				return HttpResponseRedirect(reverse(str(next_page))+"?address_added=True")
# 	else:
# 		raise Http404