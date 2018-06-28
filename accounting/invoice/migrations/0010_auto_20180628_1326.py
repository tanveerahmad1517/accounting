# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-28 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_auto_20180123_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicetemplate',
            name='numbering_scheme',
            field=models.CharField(choices=[('%Y-%m', 'yyyy-mm (2018-01)'), ('{number}', '{number} (42, for the 42nd invoice)'), ('%Y-%m-{number}', 'yyyy-mm-{number} (2018-01-42, for the 42nd invoice)'), ('%Y-%m-01', 'yyyy-mm-01 (2018-01-01, 2018-02-01 etc.)'), ('OC-%Y-%m', 'OC-yyyy-mm (OC-2018-01)'), ('OC-{number}', 'OC-{number} (OC-42, for the 42nd invoice)')], default='%Y-%m', help_text='The numbering scheme used to determine how to increment the invoice number.', max_length=80),
        ),
    ]