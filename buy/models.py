# models.py (buy)

from django.db import models
from blog.models import Post
from django.contrib.auth.models import User

class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buy by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class BuyItem(models.Model):
    buy = models.ForeignKey(Buy, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.post.title}, buy of {self.buy.created_at.strftime('%Y-%m-%d %H:%M:%S')} {self.buy.user}"
