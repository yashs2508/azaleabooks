from django.urls import path
from . import views

urlpatterns = [
		path('checkout',views.checkout,name="checkout"),
		path('',views.orders,name="user_orders"),
		path('order_history/',views.orderHistory, name="order_history"),
		path('order_details/<int:id>',views.orderDetails, name="order_details")

]