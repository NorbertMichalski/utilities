from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import KscdirectScraper
from time import sleep
from datetime import date
import csv


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        brand = Brand.objects.get(name='Dodge')
        competitor = Competitor.objects.get(name='kscdirect')
        # scraper = KscdirectScraper()
        # scraper.scrap()
        with open('/home5/shopmroc/utilities/prices/management/commands/kscdirect_results.csv', 'rb') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                print row
                price = row[2]
                if price == 0:
                    continue
                try:
                    product = Product.objects.get(part_number=row[1])
                except:
                    print 'no product'
                    continue

                try:
                    existing_result = Result.objects.get(product=product, competitor=competitor)
                    archive = Archive(product=existing_result.product, competitor=competitor, price=existing_result.price, scraped=existing_result.scraped)
                    archive.save()
                    print price, existing_result.price
                    existing_result.scraped = date.today()
                    if float(price) == float(existing_result.price):
                        existing_result.changed = False
                        existing_result.save()
                        print 'price not changed'
                        continue

                    existing_result.price = price
                    existing_result.changed = True
                    if product.mro_price < price:
                        existing_result.is_cheaper = False
                    else:
                        existing_result.is_cheaper = True
                        existing_result.product.is_cheaper = True
                    existing_result.save()
                    print 'succesfully updated product and archive'
                except:
                    result = Result(product=product, competitor=competitor)
                    result.price = price
                    result.changed = False
                    if product.mro_price < price:
                        result.is_cheaper = False
                    else:
                        result.is_cheaper = True
                        result.product.is_cheaper = True
                    result.save()
                    print 'succesfully inserted new result'
