# Generated by Django 2.2.6 on 2019-10-20 03:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0020_auto_20191019_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_city',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 20, 3, 36, 2, 175268, tzinfo=utc)),
        ),
    ]