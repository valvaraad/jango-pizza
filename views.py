# views.py (buy)

from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from .models import Buy, BuyItem
from blog.models import Post, Special, SpecialCondition, Bonuses
from cart.models import Cart, CartItem

def buy_list(request):
    promo_code = request.POST.get('promo_code')
    today = timezone.now()
    promo_applied = True

    cart, created = Cart.objects.get_or_create(user=request.user) 
    CartItems = CartItem.objects.filter(cart=cart)

    try:
        special = Special.objects.get(
            promocode=promo_code,
            start_date__lte=today,
            end_date__gte=today
        )
    except Special.DoesNotExist:
        special = None
        promo_applied = False

    print(special)
    print(promo_applied)

    special_conditions = SpecialCondition.objects.filter(special=special)
    print(special_conditions)

    if promo_applied:
        for condition in special_conditions:
            if condition.name == 'weekday':
                if int(condition.value) != today.weekday() + 1:
                    promo_applied = False
                    break
            if condition.name == 'quantity':
                if int(condition.value) > CartItems.count():
                    promo_applied = False
                    break
    
    total_cost = sum([float(buy.post.cost.replace(',', '.'))*buy.quantity for buy in CartItems ])
    
    if promo_applied:
        total_cost = total_cost - total_cost * (special.discount / 100)
    elif promo_code:
        promo_code = "не работает"
    else:
        promo_code = None

    return render(request, 'buy_list.html', {'buys': CartItems, 'total_cost': total_cost, 'promo_code': promo_code})

def promos(request):
    today = timezone.now()
    promos = Special.objects.all().order_by('-end_date')  # Сначала акции, которые скоро заканчиваются
    print(promos)
    
    return render(request, 'promos.html', {'specials': promos})


def add_to_cart(request, post_id):
    post = Post.objects.get(id=post_id)
    
    # Получаем или создаем корзину для текущего пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Пытаемся найти существующий CartItem для данной корзины и поста
    cart_item = CartItem.objects.filter(cart=cart, post=post).first()

    if cart_item:
        # Если CartItem найден, увеличиваем его quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Если CartItem не найден, создаем новый с quantity=1
        cart_item = CartItem.objects.create(cart=cart, post=post, quantity=1)

    return redirect('home')


def delete_buy(request, buy_id):
    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartItem = CartItem.objects.get(cart=cart, id=buy_id)
        cartItem.delete()
        return redirect('buy_list')

def checkout(request):
    if request.method == "POST":
        existing_cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=existing_cart)
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('buy_list')

        buy = Buy.objects.create(user=request.user)
        [BuyItem.objects.create(buy=buy, post=item.post, quantity=item.quantity) for item in cart_items]
        bonuses = Bonuses.objects.get(user=request.user)
        bonuses.bonus_count = sum([float(item.post.cost.replace(',', '.'))*int(item.quantity) for item in cart_items]) / 10
        bonuses.save()
        cart_items.delete()

        messages.success(request, "Purchase completed successfully!")
        return redirect('buy_list')
    
    return redirect('buy_list')



