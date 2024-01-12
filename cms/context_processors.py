from .models import Category
from .models import Cart, CartItem

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)



def counter(request):
    cart_count = 0
    try:
        cart_items = CartItem.objects.all().filter(cart__user=request.user)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)