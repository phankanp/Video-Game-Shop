# Generated by Django 2.2.6 on 2019-10-09 05:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20191008_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 9, 5, 57, 50, 821728, tzinfo=utc)),
        ),
    ]