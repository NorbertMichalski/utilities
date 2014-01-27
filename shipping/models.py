from django.db import models
from django import forms

# Create your models here.

class Shipping(models.Model):
    zipcode1 = models.PositiveIntegerField()
    zipcode2 = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    # part_number = models.CharField(max_length=50)
    date1 = models.DateField()
    carrier = models.CharField(max_length=50)


class InputForm(forms.Form):
    zipcode1 = forms.IntegerField()
    zipcode2 = forms.IntegerField()
    weight = forms.IntegerField()
    # part_number = forms.CharField(max_length=50)
    date1 = forms.DateField()
    carrier = forms.CharField(max_length=50)


class InternationalForm(forms.Form):
    zipcode1 = forms.CharField()
    zipcode2 = forms.CharField()
    from_country = forms.CharField()
    to_country = forms.CharField()
    weight = forms.FloatField()
    carrier = forms.CharField(max_length=50)