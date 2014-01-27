from django.core.management.base import BaseCommand, CommandError
from graph.models import OverviewStat, OverviewGraph
import datetime

def time_interval(start, end):
    delta = datetime.timedelta(days=1)
    curr = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    while curr < datetime.datetime.strptime(end, '%Y-%m-%d').date():
        yield curr
        curr += delta


class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'scrap'

    def handle(self, *args, **options):
    #def daily_graph(*args, **options):
       print 'start'
       today = datetime.date.today()
       yesterday = today - datetime.timedelta(days=1)
       try:
           date1 = args[0]
           date2 = args[1]
           dates = time_interval(date1,date2)
       except Exception as e:
           print e
           dates = [yesterday, today]
       graphs = OverviewGraph.objects.all()[:5]
       for date in dates:
           print date
           for graph in graphs:
               print graph
               try:
                   daily_stat = OverviewStat.objects.get(graph=graph, date=date)
               except Exception as e:
                   #print e
                   daily_stat = OverviewStat()
               daily_stat.graph = graph
               daily_stat.update_price()
               daily_stat.update_visits(date)
               daily_stat.update_rank(date)
               daily_stat.update_sales(date)
               if graph.brand == 'All':
                   daily_stat.update_money(date)
               daily_stat.date = date
               daily_stat.save()
               print 'successfully saved ', daily_stat
       print 'finished'