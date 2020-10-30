from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name="home"),
	path('buy/',views.buy,name="Buy"),
	path('rentals/',views.rentals,name="Rent"),
	path('about/',views.about,name="about"),
	path('contact/',views.contact,name="contact"),
	path('s/',views.search,name="Search"),
	path('<int:id>/',views.productview,name="product_view"),
	path('rentalsFAQ',views.rentalFAQ,name="rentals_policy"),
]