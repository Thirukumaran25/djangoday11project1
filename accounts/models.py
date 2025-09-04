from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.

def avatar_upload_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.username