from django.db import models
from django.db.models.deletion import CASCADE

class Receipt(models.Model):
    musician = models.ForeignKey("Musician", on_delete=CASCADE)
    business_name = models.CharField(max_length=50)
    business_address = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    date = models.DateField(auto_now=False, auto_now_add=False)
    price = models.FloatField()
    receipt_number = models.IntegerField()