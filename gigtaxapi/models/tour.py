from django.db import models
from django.db.models.deletion import CASCADE

class Tour(models.Model):
    musician = models.ForeignKey("Musician", on_delete=CASCADE)
    artist = models.CharField(max_length=50)
    tour_departure_address = models.CharField(max_length=100)
    location_address = models.CharField(max_length=100)
    tour_description = models.CharField(max_length=150)
    number_of_gigs = models.IntegerField()
    per_diem = models.FloatField()
    travel_days = models.IntegerField()
    travel_day_pay = models.FloatField()
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    date_end = models.DateField(auto_now=False, auto_now_add=False)
    tour_gig_pay = models.FloatField()
    mileage = models.IntegerField()