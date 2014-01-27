from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Result, Archive
from email_templates import EmailSender
import csv
import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print 'start'
        log.info('job start')
        all_results = Result.objects.all().prefetch_related('product')
        brands = Brand.objects.all()
        files = []
        counter = {}
        for brand in brands:
            f = open('/home5/shopmroc/utilities/reports/%s_changes.csv' % brand.name, 'wb')
            writer = csv.writer(f, dialect='excel')
            data = ['Brand', 'Competitor', 'MRO id', 'Part Number', 'MRO Price', 'New Price',
                    'Date Scraped', 'Old Price', 'Previous Date', 'Percentage Change' ]
            writer.writerow(data)
            f.close()
            counter[brand.name] = 0

        for result in all_results:
            if result.changed:
                product_id = result.product
                competitor_id = result.competitor
                mro_id = result.product.mro_id
                part_number = result.product.part_number
                competitor = result.competitor.name
                brand = result.product.brand.name
                price = result.price
                old_price = result.previous_price()
                mro_price = result.MRO_price()
                previous_date = result.previous_date()
                date = result.scraped
                percentage_changed = result.percentage_change()

                f = open('/home5/shopmroc/utilities/reports/%s_changes.csv' % brand, 'ab')
                writer = csv.writer(f, dialect='excel')
                data = [brand, competitor, mro_id, part_number,mro_price, price, date, old_price, previous_date, percentage_changed ]
                writer.writerow(data)
                f.close()
                counter[brand] += 1
                log.info(data)

        for brand in brands:
            EmailSender(brand.name, 'changes', counter[brand.name])
        log.info('Successfully finished')
        print 'finished'

