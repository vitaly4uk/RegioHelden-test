# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import rhusers.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IBANProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('country_code', models.CharField(validators=[rhusers.models.country_name_validator], max_length=2, verbose_name='country code')),
                ('check_digits', models.DecimalField(decimal_places=0, max_digits=2, verbose_name='check digits')),
                ('bban', models.CharField(max_length=30, verbose_name='basic bank account number')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
        ),
    ]
