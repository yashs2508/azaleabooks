from django.contrib import admin

# Register your models here.
from .models import EmailConfirmed
# from .models import UserAddress, UserDefaultAddress


# class UserAddressAdmin(admin.ModelAdmin):
# 	class meta:
# 		model = UserAddress

# admin.site.register(UserAddress, UserAddressAdmin)

# admin.site.register(UserDefaultAddress)
# admin.site.register(UserStripe) have to import userstripe as well at the top
admin.site.register(EmailConfirmed)