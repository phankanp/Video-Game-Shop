# Generated by Django 3.0.3 on 2020-02-17 00:46

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0021_auto_20191019_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='developer',
        ),
        migrations.AddField(
            model_name='game',
            name='developers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
    ]
