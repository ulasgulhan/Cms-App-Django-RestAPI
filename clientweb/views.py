from django.db.models import Q
from django.shortcuts import render
from cms.models import Product

# Create your views here.

def home(request):
    products = Product.objects.filter(Q(status='Active') | Q(status='Modified')).order_by('-created_date')[:8]

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)
