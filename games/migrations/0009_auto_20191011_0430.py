# Generated by Django 2.2.6 on 2019-10-11 11:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20191010_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='box_art',
            field=models.ImageField(default='video_game_store_app/img/no-image.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 11, 11, 30, 16, 822607, tzinfo=utc)),
        ),
    ]