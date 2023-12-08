from django.db import models

class Genre(models.Model):
    label = models.CharField(max_length=155)