# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-23 01:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transferwise', '0002_auto_20180116_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferwisebulkpayment',
            name='auto_create_csv_on_save',
        ),
        migrations.RemoveField(
            model_name='transferwisebulkpayment',
            name='auto_create_payments_on_save',
        ),
        migrations.RemoveField(
            model_name='transferwisebulkpayment',
            name='auto_upload_google_drive_on_save',
        ),
        migrations.RemoveField(
            model_name='transferwisebulkpayment',
            name='sender',
        ),
    ]
