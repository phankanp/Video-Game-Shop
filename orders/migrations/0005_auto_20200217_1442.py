# Generated by Django 3.0.3 on 2020-02-17 22:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200217_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 2, 17, 22, 42, 14, 749680, tzinfo=utc)),
        ),
    ]
