# Generated by Django 2.2.6 on 2019-10-12 08:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_auto_20191012_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 12, 8, 34, 2, 885537, tzinfo=utc)),
        ),
    ]
