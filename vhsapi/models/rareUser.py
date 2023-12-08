from django.contrib.auth.models import User
from django.db import models

class RareUser(models.Model):
    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    bio = models.CharField(max_length=2500)
    profile_img_url = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)