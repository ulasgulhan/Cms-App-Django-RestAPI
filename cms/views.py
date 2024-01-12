from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem, Category, Product, SubCategory, Variations
from .forms import RegisterForm

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

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    variation_ids = request.POST.getlist('variations', [])
    variations = Variations.objects.filter(id__in=variation_ids)
    cart_item.variation.set(variations)

  
    cart.save()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_item=None):
    cart_items = CartItem.objects.none()
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(cart__user=request.user)
    else:
        pass
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'cart.html', context)


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

