from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 180)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title