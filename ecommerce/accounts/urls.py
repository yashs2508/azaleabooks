from django.urls import path
from . import views

urlpatterns = [
		path('login/',views.login_view,name="auth_login"),
		path('logout/',views.logout_view,name="auth_logout"),
		path('register/',views.registration_view,name="auth_register"),
		path('activate/<activation_key>/', views.activation_view, name="activation_view" )
]