# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20180104_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinvoice',
            name='pdf_path',
            field=models.URLField(blank=True, help_text='The absolute URL that can be used to retrieve the invoice PDF.', null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='pdf_path',
            field=models.URLField(blank=True, help_text='The absolute URL that can be used to retrieve the invoice PDF.', null=True),
        ),
    ]
