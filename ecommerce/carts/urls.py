from django.urls import path
from . import views

urlpatterns = [
	path('',views.view,name="view"),
	path('cart/add/<int:id>',views.add_to_cart,name="add_to_cart"),
	path('cart/remove/<int:id>',views.remove_from_cart,name="remove_from_cart"),

]

