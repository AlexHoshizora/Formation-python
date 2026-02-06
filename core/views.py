from django.shortcuts import render

def home(request):
    return render(request, "core/index.html")

def programme(request):
    return render(request, "core/programme.html")

def paiement(request):
    return render(request, "core/paiement.html")

def contact(request):
    return render(request, "core/contact.html")