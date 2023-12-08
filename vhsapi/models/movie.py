from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=300)
    release_year = models.IntegerField()
    starring = models.CharField(max_length=600)
    director = models.CharField(max_length=200)
    genre = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')
    production_studio = models.CharField(max_length=250)
    cover_img_url = models.URLField(null=True, blank=True)
    is_available = models.BooleanField(default=False)