from django.db import models

class Rental(models.Model):
    is_selected = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_rented = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)
    returned_yet = models.BooleanField(default=False)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='user_rentals')

