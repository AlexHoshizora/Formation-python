from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("programme/", views.programme, name="programme"),
    path("paiement/", views.paiement, name="paiement"),
    path("contact/", views.contact, name="contact"),
]