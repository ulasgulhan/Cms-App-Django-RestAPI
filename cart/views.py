from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cms.models import Cart, CartItem, Product, Variations

# Create your views here.

@login_required(login_url='login')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variations.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass   

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    
        cart_item.variation.set(product_variation)
  
        cart.save()
        return redirect('cart')
    else:
        pass

    



def cart(request, total=0, quantity=0, cart_item=None):
    cart_items = CartItem.objects.none()
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(cart__user=request.user)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
    else:
        pass
    
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


def discard_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

