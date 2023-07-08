from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact_us,name="contact_us"),
    path('about',views.about_us,name="about"),
]
