from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    level = models.IntegerField(blank=True, default=0)
    experience_points = models.IntegerField(blank=True, default=0)

