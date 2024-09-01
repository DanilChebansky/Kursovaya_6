from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name="Электронная почта")
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(max_length=600, verbose_name='Комментарий')
    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return self.name

    class Meta:
        verbose_name = 'Клиент'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Клиенты'  # Настройка для наименования набора объектов


class Message(models.Model):
    head = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(max_length=600, verbose_name='Тело письма')
    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return self.head

    class Meta:
        verbose_name = 'Сообщение'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Сообщения'  # Настройка для наименования набора объектов


class Mailing(models.Model):
    PERIOD = (
        (1, 'once a minute',),
        (5, 'once in five minutes',),
        (60, 'once an hour',),
        (1440, 'once a day',),
    )
    STATUS = (
        (1, 'Created',),
        (2, 'Working...',),
        (3, 'Completed'),
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиенты')
    first_mailing_date = models.DateTimeField(verbose_name='Дата и время первой отправки рассылки', auto_now_add=True)
    next_mailing_date = models.DateTimeField(verbose_name='Дата и время следующей отправки рассылки', **NULLABLE)
    period = models.IntegerField(choices=PERIOD, default=1, verbose_name='Периодичность отправки')
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='Статус рассылки')
    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, **NULLABLE)
    is_active = models.BooleanField(verbose_name="Активная ли рассылка", default=True)

    def __str__(self):
        # Строковое отображение объекта
        return f'Рассылка сообщения с темой {self.message}'

    class Meta:
        verbose_name = 'Рассылка'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Рассылки'  # Настройка для наименования набора объектов
        permissions = [
            ('can_view_mailing_detail', 'Can view mailing details',),
            ('set_active', 'Can activate/deactivate mailing',)
        ]


class MailAttempt(models.Model):
    attempt_time = models.DateTimeField(verbose_name='Дата последней попытки', auto_now=True)
    status = models.BooleanField(verbose_name='Cтатус попытки', default=True)
    server_answer = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mail = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')

    def __str__(self):
        # Строковое отображение объекта
        str_status = ''
        if self.status:
            str_status += 'Успешно'
        else:
            str_status += 'Неудачно'
        return f'Статус попытки: {str_status}'

    class Meta:
        verbose_name = 'Попытка рассылки'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Попытки рассылки'  # Настройка для наименования набора объектов
