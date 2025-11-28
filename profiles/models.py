from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # accounts.User를 참조
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(max_length=50, unique=True)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nickname} ({self.user.username})"
    
