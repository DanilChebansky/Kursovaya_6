# Generated by Django 4.2.2 on 2024-09-01 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0005_client_owner_mailing_owner_message_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('can_view_mailing_detail', 'Can view mailing details'), ('set_active', 'Can active/disactive mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активная ли рассылка'),
        ),
    ]
