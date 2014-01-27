from django.core.management.base import BaseCommand, CommandError
from django.core import management
from prices.tools.models import Proxy, ProxyRotator
import requests
import json

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        total = Proxy.objects.count()
        proxies = Proxy.objects.all()
        count = 0
        for proxy in proxies:
            print str(proxy)
            proxy_obj = eval(str(proxy))
            try:
                resp = requests.get('http://www.dvice.com', proxies=proxy_obj)
                print resp.status_code
                if resp.status_code == 407:
                    print 'bad proxy'
                    count += 1
            except Exception as e:
                print e

        self.stdout.write('Successfully finished')
        print count
        print total
