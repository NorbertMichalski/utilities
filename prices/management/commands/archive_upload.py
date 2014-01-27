from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Result, Archive


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        all_archive = Result.objects.all()
        for archive in all_archive:
            archive.changed = False
            archive.save()

        self.stdout.write('Successfully finished')
