from django.shortcuts import render

# Create your views here.
def product_list(request):
    return render(request, "product_list.html")

def product_type(request):
    return render(request, "product_type.html")
