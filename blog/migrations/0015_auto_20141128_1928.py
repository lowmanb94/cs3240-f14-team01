# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20141128_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='myFile',
            field=models.FileField(upload_to=b'files'),
            preserve_default=True,
        ),
    ]
