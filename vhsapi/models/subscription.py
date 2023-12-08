from django.db import models

class Subscription(models.Model):
    created_on = models.DateField(auto_now_add=True)
    ends_on = models.DateField()
    card_number = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE)