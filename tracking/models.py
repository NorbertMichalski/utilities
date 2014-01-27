from django.db import models
from django import forms

# Create your models here.

class Shipping(models.Model):
    orderNumber = models.CharField(max_length=50)
    trackNumber = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    dateAdded = models.DateTimeField('date introduced')
    
    def __unicode__(self):
        return self.orderNumber
    
    def bostonGear(self):
        pass
    
    def baldorVip(self):
        pass
    

class InputForm(forms.Form):
    codes = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100)