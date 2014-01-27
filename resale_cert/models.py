from django.db import models
from django import forms
import datetime

# Create your models here.

class Reseller(models.Model):
    permit_number = models.CharField(max_length=50)
    validation = models.CharField(max_length=20)
    owner = models.CharField(max_length=100)
    bussiness_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=5)
    start_date = models.DateField(default=datetime.date.today, blank=True)

    def __unicode__(self):
        return self.validation

    def write_output(self, dictionary):
        if type(dictionary) is dict:
            try:
                Reseller.objects.get(permit_number=dictionary['permit_no'])
            except Reseller.DoesNotExist:
                reseller = Reseller()
                reseller.permit_number = dictionary['permit_no']
                reseller.validation = dictionary['valid']
                reseller.owner = dictionary['owner']
                reseller.business_name = dictionary['bussiness_name']
                reseller.address = dictionary['address']
                reseller.city = dictionary['city']
                reseller.state = dictionary['state']
                if dictionary['start_date']:
                    reseller.start_date = dictionary['start_date']
                reseller.save()
            else:
                pass


class InputForm(forms.Form):
    permit_number = forms.IntegerField()