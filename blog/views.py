from django.views.generic import ListView, DetailView, TemplateView 

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Bonuses, BonusShopItem
import asyncio
from blog.models import Post
 
 
class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class BonusShopView(ListView):
    model = BonusShopItem
    template_name = 'home.html'


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                user = User.objects.create_user(username, email, password)
                Bonuses.objects.create(user=user)
                return redirect(reverse("login"))

        return render(request, self.template_name)


class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request):
        bonuses = Bonuses.objects.get(user=request.user)

        return render(request, self.template_name, {'bonuses': bonuses})




from cart.forms import CartAddProductForm


def product_detail(request, id, slug):
    product = get_object_or_404(Post,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})