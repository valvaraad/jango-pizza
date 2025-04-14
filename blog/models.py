from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


 
 
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    cost = models.CharField(max_length=200)
    
 
    def __str__(self):
        return self.title

class BonusShopItem(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='images/')
    cost = models.CharField(max_length=200)
    
 
    def __str__(self):
        return self.title

class SpecialCondition(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} ({self.value})"

class Special(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    promocode = models.CharField(max_length=8)
    condition = models.ManyToManyField(SpecialCondition)
    discount = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.name

class Bonuses(models.Model):
    bonus_count = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Кол-во бонусов: {self.bonus_count}"

