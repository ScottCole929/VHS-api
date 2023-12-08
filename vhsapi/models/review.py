from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=150)
    comment = models.CharField(max_length=3000)
    date_reviewed = models.DateField(auto_now_add=True)
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='user_reviews')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
