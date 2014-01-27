from celery import task
from graph.models import OverviewStat, OverviewGraph
import datetime
from django.utils import timezone
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def time_interval(start, end):
    delta = datetime.timedelta(days=1)
    curr = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    while curr < datetime.datetime.strptime(end, '%Y-%m-%d').date():
        yield curr
        curr += delta

@task
def daily_graph(*args, **options):
    logger.info('start')
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    try:
        date1 = args[0]
        date2 = args[1]
        dates = time_interval(date1,date2)
    except Exception as e:
        logger.info(e)
        dates = [yesterday, today]
    graphs = OverviewGraph.objects.all()[:5]
    for date in dates:
        logger.info(date)
        for graph in graphs:
            logger.info(graph)
            try:
                daily_stat = OverviewStat.objects.get(graph=graph, date=date)
            except Exception:
                daily_stat = OverviewStat()
            daily_stat.graph = graph
            daily_stat.update_price()
            daily_stat.update_visits(date)
            daily_stat.update_rank(date)
            daily_stat.update_sales(date)
            daily_stat.update_money(date)
            daily_stat.date = date
            daily_stat.save()
    logger.info('finished')


@task
def graph_report(*args, **options):
    pass
