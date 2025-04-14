from django.urls import path

from .views import BlogListView, BlogDetailView 
from buy import views
 
urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('add_to_cart/<int:post_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy/', views.buy_list, name='buy_list'),
]