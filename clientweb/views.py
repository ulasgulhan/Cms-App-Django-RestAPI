from django.shortcuts import render
from cms.models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(status='Active')

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)
