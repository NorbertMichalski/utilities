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
        log.info('start job')
        all_results = Result.objects.all().prefetch_related('product')
        brands = Brand.objects.all()
        files = []
        counter = {}
        for brand_name in brands:
            f = open('/home5/shopmroc/utilities/reports/%s_cheaper.csv' % brand_name, 'wb')
            writer = csv.writer(f, dialect='excel')
            data = ['Brand', 'Competitor', 'MRO id', 'Part Number', 'Our Price', 'Their Price' ]
            writer.writerow(data)
            f.close()
            counter[brand_name.name] = 0

        for result in all_results:

            if result.is_cheaper:
                product_id = result.product
                if not product_id.is_cheaper:
                    product_id.is_cheaper = True
                    product_id.save()
                mro_id = result.product.mro_id
                part_number = result.product.part_number
                competitor = result.competitor.name
                brand = result.product.brand.name
                price = result.price
                mro_price = result.product.mro_price

                f = open('/home5/shopmroc/utilities/reports/%s_cheaper.csv' % brand, 'ab')
                writer = csv.writer(f, dialect='excel')
                data = [brand, competitor, mro_id, part_number, mro_price, price ]
                writer.writerow(data)
                f.close()
                counter[brand] += 1
                log.info(data)


        for brand in brands:
            EmailSender(brand.name, 'cheaper', counter[brand.name])

        log.info('Successfully finished')



