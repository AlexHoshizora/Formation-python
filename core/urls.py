from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("programme/", views.programme, name="programme"),
    path("paiement/", views.paiement, name="paiement"),
    path("contact/", views.contact, name="contact"),
    path("connexion/", views.connexion, name="connexion"),
    path("espace/", views.dashboard, name="dashboard"),
    path("module/0/installation-python/", views.module_0_installation, name="module_0_installation"),
]