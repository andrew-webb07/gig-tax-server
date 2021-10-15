from django.db import models
from django.db.models.deletion import CASCADE

class Gig(models.Model):
    musician = models.ForeignKey("Musician", on_delete=CASCADE)
    artist = models.CharField(max_length=50)
    location_name = models.CharField(max_length=50)
    location_address = models.CharField(max_length=100)
    gig_description = models.CharField(max_length=150)
    date = models.DateField(auto_now=False, auto_now_add=False)
    gig_pay = models.FloatField()
    mileage = models.IntegerField()
