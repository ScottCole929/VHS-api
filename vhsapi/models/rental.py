from django.db import models

class Rental(models.Model):
    date_rented = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)
    returned_yet = models.BooleanField(default=False)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='user_rentals')

