# Generated by Django 2.2.6 on 2019-10-14 00:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0016_auto_20191012_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 14, 0, 4, 57, 151623, tzinfo=utc)),
        ),
    ]
