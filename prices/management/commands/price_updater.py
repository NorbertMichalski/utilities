from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result
import csv

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, file, *args, **options):
        with open(file, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in csvreader:
                mro_id = row[0]
                try:
                    product = Product.objects.get(mro_id=mro_id)
                    product.mro_price = row[1]
                    product.save()
                    print 'updated %s with price %s' % (product, product.mro_price)
                except:
                    continue

        self.stdout.write('Successfully finished')
