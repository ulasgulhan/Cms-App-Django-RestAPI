from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.http.response import ResponseHeaders
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Product, SubCategory
from .forms import ProductCreateForm, RegisterForm
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode
from django.core.paginator import Paginator


# Create your views here.


def store(request, category_slug=None, subcategory_slug=None):
    if subcategory_slug != None:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = Product.objects.filter(Q(category=subcategory), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        return render(request, 'store.html', {'products': paged_products, 'product_count': product_count, 'subcategory': subcategory})
    elif category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = category.subcategories.all()
        products = Product.objects.filter(Q(category__in=subcategories), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        return render(request, 'store.html', {'products': paged_products, 'product_count': product_count, 'category': category})
    else:
        products = Product.objects.filter(Q(status='Active') | Q(status='Modified')).order_by('created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        return render(request, 'store.html', {'products': paged_products, 'product_count': product_count})


def product_details(request, category_slug, subcategory_slug, product_slug):
    single_product = get_object_or_404(Product, Q(category__slug=subcategory_slug), Q(slug=product_slug), Q(status='Active') | Q(status='Modified'))
    context = {
        'single_product': single_product
    }
    return render(request, 'product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword), Q(status='Active') | Q(status='Modified'))
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
    products = Product.objects.select_related('category').filter(Q(supplier=request.user), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
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
        product.status = 'Passive'
        product.save()
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
                product.status = 'Modified'
                form.save()
                return redirect('dashboard')
    else:
        form = ProductCreateForm(instance=product)
    
    context = {
        'form': form
    }
    
    return render(request, 'dashboard/update.html', context)


def supplier_store(request, user_id):
    supplier = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(Q(supplier=supplier), Q(status='Active') | Q(status='Modified')).order_by('-created_date')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
        'supplier': supplier,
    }

    return render(request, 'store.html', context)


def profile(request):
    return render(request, 'dashboard/profile.html')


def permissions(request):
    users = User.objects.filter(is_active=True).order_by('-username')
    if request.user.is_superuser:
        return render(request, 'dashboard/permissions.html', {'users': users})
    else:
        return HttpResponse('Unauthorized', status=403)



def permissio_change(request, user_id):
    login_user = request.user
    user = get_object_or_404(User, Q(id=user_id), Q(status='Active') | Q(status='Modified'))
    if login_user.is_superuser:
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
    else:
        messages.error(request, 'You are not allowed to change this user.')
    return redirect('permissions')
