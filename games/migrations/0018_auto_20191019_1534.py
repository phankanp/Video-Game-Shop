# Generated by Django 2.2.6 on 2019-10-19 22:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_auto_20191013_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 19, 22, 34, 0, 808017, tzinfo=utc)),
        ),
    ]
