from django.core.mail import EmailMessage
import logging
log = logging.getLogger(__name__)


class EmailSender(object):

    messages = {'changes': ' report with all the competitors that modified their prices during last week',
                'cheaper': ' report with all the competitors that have their prices lower than ours.',
                }
    intro = 'Hi Matt \n\nThis is the weekly '

    def __init__(self, brand, report_type, number_results):
        titles = {'changes': (' automated report: found %s price changes this week' % number_results),
                  'cheaper': (' automated report: found %s cheaper prices this week' % number_results),
                  }
        self.subject = brand.capitalize() + titles[report_type]
        self.body = self.intro + brand.capitalize() + self.messages[report_type]

        email = EmailMessage(self.subject, self.body, 'reports@shopmro.com', ['stats.infographics@gmail.com', 'mmenashe@mechdrives.com' ])
        # 'mmenashe@mechdrives.com'
        if number_results > 0:
            email.attach_file('/home5/shopmroc/utilities/reports/%s_%s.csv' % (brand.capitalize(), report_type))
        email.send(fail_silently=False)
        log.info('email sent succesfully')
