# urls.py (buy)

from django.urls import path
from views import *

urlpatterns = [
    path('buy/', buy_list, name='buy_list'),
    path('add_to_cart/<int:post_id>/', add_to_cart, name='add_to_cart'),
    path('delete_buy/<int:buy_id>/', delete_buy, name='delete_buy'),
    path('checkout/', checkout, name='checkout'),
]
