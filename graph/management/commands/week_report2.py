from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from graph.models import OverviewStat, OverviewGraph
from prices.models import Brand, Result
import datetime
import csv


def send_email(file_attached):
    subject = "weekly report"
    body = "Attached is the weekly statistics report."
    email = EmailMessage(subject, body, 'reports@shopmro.com',
                          ['stats.infographics@gmail.com', 'mmenashe@mechdrives.com' ])
    email.attach_file(file_attached)
    email.send(fail_silently=False)

def weekly_stats(graph_pk):
    stats = OverviewStat.objects.filter(graph=graph_pk).order_by('date')
    current_week = stats[0].date.isocalendar()[1]
    weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
    counter = 1
    for stat in stats:
        week = stat.date.isocalendar()[1]
        if week != current_week:
            break
        weekly_money += float('%.2f' %stat.get_money())
        weekly_price += float('%.2f' %(stat.get_price()/10,))
        weekly_rank += stat.get_rank()
        weekly_visits += stat.get_visits()
        weekly_sales += stat.get_sales()
        counter += 1
    return weekly_visits, weekly_sales, weekly_money, int(weekly_rank/counter)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # override last week's report
        f = open('/home5/shopmroc/utilities/reports/weekly_report.csv', 'wb')
        writer = csv.writer(f, dialect='excel')
        data = ['Brand', 'Total visits', 'Average visits', 'Total sales', 'Average sales',
                'Prices changed', 'Number prices changes', 'Average rank' ]
        writer.writerow(data)
        f.close()
        # count the changes of prices
        brands = Brand.objects.all()
        counter = {'All':0}
        for brand in brands:
            counter[brand.name] = 0
        all_results = Result.objects.all().prefetch_related('product')
        for result in all_results:
            if result.changed:
                brand_name = result.product.brand.name
                counter[brand_name] += 1
        print counter
        sales, visits = [], []
        prices_changed, rank_changed = False, False
        # if not monday get last moday's report
        today = datetime.date.today()
        week_day = today.weekday() 
        if week_day:
            today = today - datetime.timedelta(days=week_day)
        print today
        # get all brands
        graphs = OverviewGraph.objects.all()[:5]
        f = open('/home5/shopmroc/utilities/reports/weekly_report.csv', 'ab')
        writer = csv.writer(f, dialect='excel')
        for graph in graphs:
            try:
                counter[graph.brand]
            except KeyError:
                continue
            if counter[graph.brand]:
                prices_changed = 'Yes'
            else:
                prices_changed = 'No'
            # get the week statistics
            weekly_visits, weekly_sales, weekly_money, weekly_rank = weekly_stats(graph.pk)
            data = [graph.brand, weekly_visits, weekly_visits/7, weekly_sales,
                    weekly_sales/7, prices_changed, counter[graph.brand], weekly_rank,
                    ]
            if graph.brand == 'All':
                total_sales = weekly_money
                data = ['All brands', weekly_visits, weekly_visits/7, weekly_sales,
                        weekly_sales/7, '', '', weekly_rank,]
            writer.writerow(data)
        writer.writerow([])
        data = ['Total profit', total_sales]
        writer.writerow(data)
        data = ['Average day profit', '%.2f' %(total_sales/7,)]
        writer.writerow(data)
        f.close()
        send_email('/home5/shopmroc/utilities/reports/weekly_report.csv')
