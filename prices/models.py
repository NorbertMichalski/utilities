from django.db import models
import datetime

# Create your models here.
class Competitor(models.Model):
    name = models.CharField('Competitor', max_length=100, unique=True)
    website = models.CharField(max_length=100)
    last_scrap = models.DateField('date last scraped', default=datetime.date.today)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField('Brand', max_length=100)
    competitor = models.ManyToManyField(Competitor)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand)
    mro_id = models.IntegerField(unique=True)
    part_number = models.CharField(max_length=100)
    mro_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    updated = models.DateField('date last updated', default=datetime.date.today)
    is_cheaper = models.BooleanField()

    def __unicode__(self):
        return self.part_number

    class Meta:
        ordering = ['mro_id']
        unique_together = (('mro_id', 'part_number'))

    competitors = Competitor.objects.all()
    for competitor in competitors:
        exec("""def %s(self):
                    competitor = Competitor.objects.get(name='%s')
                    try:
                        result = Result.objects.get(product=self.pk, competitor=competitor.pk)
                        return result.price
                    except:
                        return None""" % (competitor.name, competitor.name))


class Result(models.Model):
    product = models.ForeignKey(Product)
    competitor = models.ForeignKey(Competitor)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    scraped = models.DateField('date last scraped', default=datetime.date.today)
    is_cheaper = models.BooleanField()
    changed = models.BooleanField()

    def __unicode__(self):
        return unicode(self.price)

    def previous_price(self):
        try:
            archive = Archive.objects.filter(product_id=self.product_id, competitor_id=self.competitor_id).latest('scraped')
            return unicode(archive.price)
        except Exception as e:
            return
    
    def previous_date(self):
        try:
            archive = Archive.objects.filter(product_id=self.product_id, competitor_id=self.competitor_id).latest('scraped')
            return unicode(archive.scraped)
        except Exception as e:
            return
    
    def percentage_change(self):
        try:
            previous_price = float(str(self.previous_price()))
            #result = '%+.2f' %((previous_price - float(str(self.price))) / previous_price * 100)
            result = '%+.2f' %((float(str(self.price)) - previous_price) / previous_price * 100)
            result = result.zfill(6)
            result += ' %'
            return result
        except Exception as e:
            return
        
    def MRO_id(self):
        return self.product.mro_id
    
    def MRO_price(self):
        return self.product.mro_price
    
    def brand(self):
        return self.product.brand.name
        
class Archive(models.Model):
    product = models.ForeignKey(Product)
    competitor = models.ForeignKey(Competitor)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    scraped = models.DateField('date last scraped', default=datetime.date.today)

    class Meta:
        get_latest_by = 'scraped'

    def __unicode__(self):
        return unicode(self.price)




class BaldorReport(Product):
    readonly_fields = ('brand', 'mro_id', 'part_number', 'mro_price', 'updated')
    class Meta:
        proxy = True


class RedlionReport(Product):
    readonly_fields = ('brand', 'mro_id', 'part_number', 'mro_price', 'updated')
    class Meta:
        proxy = True


class LeesonReport(Product):
    readonly_fields = ('brand', 'mro_id', 'part_number', 'mro_price', 'updated')
    class Meta:
        proxy = True


class DodgeReport(Product):
    readonly_fields = ('brand', 'mro_id', 'part_number', 'mro_price', 'updated')
    class Meta:
        proxy = True







