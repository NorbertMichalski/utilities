from django.db import models
from django import forms
import datetime

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    brand = models.ForeignKey(Brand)
    slug = models.CharField(max_length=50)
    city_state = models.CharField(max_length=100)
    address = models.CharField(max_length=100, default='')
    zip = models.CharField(max_length=10, default='')
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.IntegerField(default=0)
    timezone = models.CharField(max_length=50)
    timediff = models.IntegerField(max_length=2, default=0)

    def __unicode__(self):
        return self.city_state


class InputForm(forms.Form):
    codes = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10, required=False)
    yourlocation = forms.CharField(max_length=100, required=False)


class Product(models.Model):
    brand = models.ForeignKey(Brand)
    mro_id = models.IntegerField()
    part_number = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    updated = models.DateField('date last updated', default=datetime.date.today)

    def __unicode__(self):
        return self.part_number




