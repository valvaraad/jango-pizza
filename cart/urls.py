from . import views
from django.urls import path
from buy.views import buy_list, checkout

urlpatterns = [
    path('$', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:post_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/(?P<post_id>\d+)/$', views.cart_remove, name='cart_remove'),
    path('buy/', buy_list, name='buy_list'),
    path('checkout/', checkout, name='checkout')

]