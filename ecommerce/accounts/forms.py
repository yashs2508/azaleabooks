from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from orders.models import UserAddress

User = get_user_model()


# class UserAddressForm(forms.ModelForm):
# 	default = forms.BooleanField(label = 'Make Default')
# 	class Meta:
# 		model = UserAddress
# 		fields = [
# 			"first_name",
# 			"last_name",
# 			"address", 
# 			"address_2", 
# 			"city", 
# 			"state", 
# 			"country", 
# 			"pincode", 
# 			"phone",
# 		]

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise forms.ValidationError("Are you sure you're registered? We couldn't find such user.")
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			user = None
		if user is not None and not user.check_password(password):
			raise forms.ValidationError("Wrong Password!")
		elif user is None:
			pass
		else:
			return password

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label = 'Email')
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not Match!")
		else:
			return password2


	def clean_email(self):
		email = self.cleaned_data.get('email')
		user_count = User.objects.filter(email = email).count()
		if user_count > 0:
			raise forms.ValidationError("This email has already been registered. Please use a different email-id.")
		return email


	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=50, required= True)
	name = forms.CharField(max_length=20, required= True)
	Email = forms.EmailField(max_length=50, required= True)
	message = forms.CharField(
				max_length=500,
				widget = forms.Textarea(),
				help_text = 'Write your message here!',
				)
