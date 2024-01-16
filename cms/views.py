from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from .models import Cart, CartItem, Category, Product, SubCategory, Variations
from .forms import ProductCreateForm, RegisterForm
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode

# Create your views here.

def store(request, category_slug=None, subcategory_slug=None):
    if subcategory_slug != None:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = Product.objects.filter(Q(category=subcategory), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
        product_count = products.count()
        return render(request, 'store.html', {'products': products, 'product_count': product_count, 'subcategory': subcategory})
    elif category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = category.subcategories.all()
        products = Product.objects.filter(Q(category__in=subcategories), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
        product_count = products.count()
        return render(request, 'store.html', {'products': products, 'product_count': product_count, 'category': category})
    else:
        products = Product.objects.all().filter(Q(status='Active') | Q(status='Modified')).order_by('-created_date')
        product_count = products.count()
        return render(request, 'store.html', {'products': products, 'product_count': product_count})



def product_details(request, category_slug, subcategory_slug, product_slug):
    single_product = Product.objects.get(category__slug=subcategory_slug, slug=product_slug)
    context = {
        'single_product': single_product
    }
    return render(request, 'product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        else:
            return redirect('home')

    context = {
            'products': products,
            'product_count': product_count,
            'keyword': keyword,
        }
    return render(request, 'store.html', context)



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = RegisterForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)

@login_required
def dashboard(request):
    products = Product.objects.select_related('category').filter(supplier=request.user).order_by('-created_date')
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = request.user
            product_name = form.cleaned_data['product_name']
            slug_candidate = unidecode(product_name)
            product.slug = slugify(slug_candidate.replace(' ', '-').lower())
            product.created_date = timezone.now()
            product.save()
            return redirect('dashboard')
    else:
        form = ProductCreateForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'dashboard/create.html', context)


@login_required
def delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.supplier == request.user:
        product.delete()
    else:
        messages.error(request, 'You are not allowed to delete this product.')
    return redirect('dashboard')


@login_required
def update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if product.supplier == request.user:
            form = ProductCreateForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    else:
        form = ProductCreateForm(instance=product)
    
    context = {
        'form': form
    }
    
    return render(request, 'dashboard/update.html', context)
