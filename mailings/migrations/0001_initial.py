# Generated by Django 4.2.2 on 2024-08-27 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, verbose_name='Электронная почта')),
                ('name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('comment', models.TextField(max_length=600, verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=150, verbose_name='Тема письма')),
                ('body', models.TextField(max_length=600, verbose_name='Тело письма')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_mailing_date', models.DateTimeField(verbose_name='Дата и время первой отправки рассылки')),
                ('period', models.CharField(choices=[('once a day ', '1'), ('once a week', '7'), ('once a month', '30')], default='once a day ', max_length=15)),
                ('status', models.CharField(choices=[('Created', '1'), ('Working...', '2'), ('Completed', '3')], default='Created', max_length=15)),
                ('client', models.ManyToManyField(related_name='mailings', to='mailings.client', verbose_name='Клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.message', verbose_name='Сообщение')),
            ],
        ),
        migrations.CreateModel(
            name='MailAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now=True, verbose_name='Дата последней попытки')),
                ('status', models.BooleanField(default=True, verbose_name='Cтатус попытки')),
                ('server_answer', models.TextField(blank=True, null=True, verbose_name='Ответ сервера')),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='mailings.mailing', verbose_name='Рассылка')),
            ],
        ),
    ]
