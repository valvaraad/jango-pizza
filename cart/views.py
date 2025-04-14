# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from blog.models import Post

@login_required
def add_to_cart(request, post_id):
    # Получаем пост (пиццу)
    post = get_object_or_404(Post, id=post_id)
    
    # Если у пользователя еще нет корзины, создаем новую
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Проверяем, есть ли уже этот пост в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, post=post)
    
    if not created:
        # Если товар уже в корзине, увеличиваем количество
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')  # Перенаправляем обратно на страницу с товарами

def checkout(request):
    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('buy_list')
        
        # Process payment/order here
        cart_items.delete()  # Clear the cart
        
        messages.success(request, "Purchase completed successfully!")
        return redirect('buy_list')
    
    return redirect('buy_list')
