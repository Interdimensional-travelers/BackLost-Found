from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('гаманці', 'Гаманці'),
        ('тваринки', 'Тваринки'),
        ('техніка', 'Техніка'),
        ('ключі', 'Ключі'),
        ('сумки', 'Сумки'),
        ('аксесуари', 'Аксесуари'),
        ('документи', 'Документи'),
        ('інше', 'Інше'),
    )
    title = models.CharField(max_length = 180)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    lost = models.BooleanField(default = True, blank = True)
    email = models.CharField(max_length = 180)
    phone = models.CharField(max_length = 180)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='інше')
    def __str__(self):
        return self.title