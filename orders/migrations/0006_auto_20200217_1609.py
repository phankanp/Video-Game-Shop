# Generated by Django 3.0.3 on 2020-02-18 00:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200217_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 2, 18, 0, 9, 24, 811673, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]