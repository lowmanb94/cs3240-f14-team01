# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 3, 22, 40, 37, 307060, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
