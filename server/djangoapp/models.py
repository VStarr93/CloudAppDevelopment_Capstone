import sys
from django.db import models
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings

import uuid


# Create your models here.

# <HINT> Create a Car Make model
class CarMake(models.Model):
# - Name
    name = models.CharField(max_length=100)
# - Description
    description = models.TextField(max_length=500)
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model 
class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
# - Name
    name = models.CharField(max_length=100)
# - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    type_choices = (
        ("SEDAN", "Sedan"),
        ("WAGON", "Wagon"),
        ("SUV", "Suv"),
    )
    type = models.CharField(max_length=20, choices=type_choices, default="SEDAN")
# - Year (DateField)
    year = models.DateField(null=True, blank=True)
# - Any other fields you would like to include in car model
    color = models.CharField(max_length=10)
# - __str__ method to print a car make object
    def __str__(self):
        return self.name
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    # an instance of this class is used to store a dealer object returned from get-dealership service
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer full name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    
    def __str__(self):
        return "Dealer name: " + self.full_name
        
# <HINT> Create a plain Python class `DealerReview` to hold review data
