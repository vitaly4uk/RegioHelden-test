# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rhusers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ibanprofile',
            name='created_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='created'),
        ),
        migrations.AlterField(
            model_name='ibanprofile',
            name='bban',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$')], max_length=30, verbose_name='basic bank account number'),
        ),
        migrations.AlterField(
            model_name='ibanprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile'),
        ),
    ]
