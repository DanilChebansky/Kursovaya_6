import smtplib

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from mailings.models import Mailing, MailAttempt


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        mailings = Mailing.objects.filter(first_mailing_date__lte=current_datetime).filter(
            status__in=[1, 2])
        for mailing in mailings:
            try:
                response = send_mail(subject=mailing.message.head,
                                     message=mailing.message.body,
                                     from_email=settings.EMAIL_HOST_USER,
                                     recipient_list=[client.email for client in mailing.client.all()],
                                     fail_silently=False)

                MailAttempt.objects.create(server_answer=str(response), mail=mailing)

            except smtplib.SMTPException as e:
                MailAttempt.objects.create(server_answer=str(e), mail=mailing, status=False)
