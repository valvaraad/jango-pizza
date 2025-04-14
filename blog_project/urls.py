"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.db import router
from django.urls import path, include 
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from blog import views
from buy.views import buy_list, delete_buy, checkout, promos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView.as_view(), name="register"),
    path('accounts/profile/', views.ProfilePage.as_view(), name="profile"),
    path('buy/', buy_list, name='buy_list'),
    path('delete_buy/<int:buy_id>/', delete_buy, name='delete_buy'),
    path('checkout/', checkout, name='checkout'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('promos/', promos, name='promos'),
    path('bonusshop/', views.BonusShopView.as_view(), name='bonus_shop')
    
    # path('add_cart/', include('cart.urls'), Page_cart.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

