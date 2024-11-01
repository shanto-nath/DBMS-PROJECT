from django.shortcuts import render,redirect
# Create your views here.

def home(request):
    return render(request, "index.html", {'about_show_more' : True})

def about(request):
    return render(request, "about.html", {'about_show_more' : False})

def faqs(request):
    return render(request, "faqs.html")

def license(request):
    return render(request, "license.html")

def terms(request):
    return render(request, "terms.html")

def testimonial(request):
    return render(request, "testimonial.html")

def notFound(request):
    return render(request, "404.html")

def contact(request):
    return render(request, 'contact.html')
