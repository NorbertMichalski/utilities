from django.db import models
import json
import datetime
import csv
from prices.models import Product, Brand
from utilities.settings import MEDIA_ROOT
import os


# Create your models here.

class Proxy(models.Model):
    address = models.IPAddressField()
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __unicode__(self):
        pass
        data = ("http://%s:%s@%s:%s" % (self.username, self.password, self.address, self.port))
        return data


class ProxyRotator(object):

    def __init__(self, *args, **kwargs):
        self.PROXY_TOTAL = Proxy.objects.count()
        self.PROXY_INDEX = 0
        self.PROXIES = Proxy.objects.all()

    def rotate_proxy(self):
        self.PROXY_INDEX += 1
        if self.PROXY_INDEX > self.PROXY_TOTAL - 1:
            self.PROXY_INDEX = 0
            print self.PROXY_INDEX
        current_proxy = self.PROXIES[self.PROXY_INDEX].__unicode__()
        print current_proxy
        data = {}
        data["http"] = current_proxy
        return json.dumps(data)


class UploadProduct(models.Model):
    csv_file = models.FileField(upload_to='products_csv', help_text='The csv file should contain only 4 columns - Brand, MRO id, part number and price (no headers required)')
    url = models.URLField(max_length=150, blank=True, help_text='The url is optional, an alternative to direct file upload')
    uploaded_at = models.DateTimeField(default=datetime.datetime.now)
    successfully_updated = models.IntegerField(default=0, blank=True, help_text='No need to complete this, here it will appear afterwards the number of succesful entries')
    failed_entries = models.TextField(default='', blank=True, help_text='No need to complete this, here it will appear afterwards the failed entries, so you can correct them')

    def __unicode__(self):
        return unicode(self.csv_file).split('/')[1]

    def save(self):
        super(UploadProduct, self).save()
        file = os.path.join(MEDIA_ROOT + str(self.csv_file))
        f = open(file, 'rb')
        reader = csv.reader(f, dialect='excel')
        counter = 0
        garbage = []
        for row in reader:
            try:
                Product.objects.get(mro_id=row[1])
                garbage.append(','.join(row))
                continue
            except:
                product = Product()
                try:
                    product.brand = Brand.objects.get(name=row[0])
                    product.mro_id = row[1]
                    product.part_number = row[2]
                    product.mro_price = float(row[3])
                    product.updated = datetime.date.today()
                    product.is_cheaper = False
                    product.save()
                    counter += 1
                except:
                    garbage.append(','.join(row))
                    continue

        self.successfully_updated = counter
        if garbage:
            self.failed_entries = '\n'.join(garbage)
        super(UploadProduct, self).save()


class UpdatePrice(models.Model):
    csv_file = models.FileField(upload_to='prices_csv', help_text='The csv file should contain only 2 columns - MRO id and price (no headers required)')
    url = models.URLField(max_length=150, blank=True, help_text='The url is optional, an alternative to direct file upload')
    uploaded_at = models.DateTimeField(default=datetime.datetime.now)
    successfully_updated = models.IntegerField(default=0, blank=True, help_text='No need to complete this, here it will appear afterwards the number of succesful entries')
    failed_entries = models.TextField(default='', blank=True, help_text='No need to complete this, here it will appear afterwards the failed entries, so you can correct them')

    def __unicode__(self):
        return unicode(self.csv_file).split('/')[1]


    def save(self):
        super(UpdatePrice, self).save()
        file = os.path.join(MEDIA_ROOT + str(self.csv_file))
        f = open(file, 'rb')
        reader = csv.reader(f, dialect='excel')
        counter = 0
        garbage = []
        for row in reader:
            try:
                product = Product.objects.get(mro_id=row[0])
                product.mro_price = float(row[1])
                product.updated = datetime.date.today()
                product.is_cheaper = False
                product.save()
                counter += 1
            except:
                garbage.append(','.join(row))
                continue
        self.successfully_updated = counter
        if garbage:
            self.failed_entries = '\n'.join(garbage)
        super(UpdatePrice, self).save()
