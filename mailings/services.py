import smtplib
from datetime import timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
from django_apscheduler.jobstores import DjangoJobStore
from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailings.models import Mailing, MailAttempt, Message


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # создание объекта с применением фильтра
    mailings = Mailing.objects.filter(first_mailing_date__lte=current_datetime).filter(
        status__in=[1]).filter(is_active=True)

    for mailing in mailings:
        if mailing.next_mailing_date is None:
            mailing.next_mailing_date = current_datetime
            mailing.save()
        if mailing.next_mailing_date <= current_datetime and mailing.next_mailing_date:
            try:
                response = send_mail(subject=mailing.message.head,
                                     message=mailing.message.body,
                                     from_email=settings.EMAIL_HOST_USER,
                                     recipient_list=[client.email for client in mailing.client.all()],
                                     fail_silently=False)

                MailAttempt.objects.create(server_answer=str(response), mail=mailing)

            except smtplib.SMTPException as e:
                MailAttempt.objects.create(server_answer=str(e), mail=mailing, status=False)
            mailing.next_mailing_date += timedelta(minutes=mailing.period)
            mailing.save()


def start():
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_mailing,
        trigger=CronTrigger(second="*/10"),  # Every 10 seconds
        id="send_mailing",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()


def get_messages_from_cache():
    """
    Получение списка сообщений из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Message.objects.all()
    else:
        key = 'categories_list'
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages)
            return messages
