# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rhusers', '0002_auto_20160801_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ibanprofile',
            name='check_digits',
            field=models.DecimalField(verbose_name='check digits', default=0, max_digits=2, decimal_places=0),
        ),
        migrations.AlterField(
            model_name='ibanprofile',
            name='created_by',
            field=models.ForeignKey(related_name='created', to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
