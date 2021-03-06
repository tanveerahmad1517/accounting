# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 14:25
from __future__ import unicode_literals

import datetime
import uuid

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields

from accounting.invoice.choices import InvoiceNumberingScheme
import accounting.common.mixins


def create_invoice_templates(apps, schema_editor):
    """
    Create invoice templates based off of the latest invoices for all providers.

    In particular, do the following:
    * Guess the numbering scheme used for the invoice number, and select the appropriate one. Falls back to the default.
    * Copy over the extra text and image to be used for future invoices.

    The HTML template isn't explicitly copied over, because at the time of this migration, no HTML template
    besides the default existed.
    """
    Account = apps.get_model('account', 'Account')
    Invoice = apps.get_model('invoice', 'Invoice')
    InvoiceTemplate = apps.get_model('invoice', 'InvoiceTemplate')
    # Only loop through those accounts that actually have invoices that need a template.
    for provider in Account.objects.filter(provider_invoices__isnull=False):
        latest_invoice = provider.provider_invoices.latest('date')

        # Guess the numbering scheme.
        number = latest_invoice.number
        numbering_scheme = InvoiceNumberingScheme.default
        for scheme in InvoiceNumberingScheme.values.keys():
            try:
                # Scheme possibly has dates.
                if number == datetime.datetime.strptime(number, scheme).strftime(scheme):
                    numbering_scheme = scheme
                    break
            except ValueError:
                # Scheme does not contain dates.
                number_value = number.split('-')[-1].lstrip('0')
                if number == scheme.format(number=number_value):
                    numbering_scheme = scheme

        template = InvoiceTemplate.objects.create(
            provider=provider,
            numbering_scheme=numbering_scheme,
            extra_text=latest_invoice.extra_text,
            extra_image=latest_invoice.extra_image,
        )
        Invoice.objects.filter(provider=provider).update(template=template)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180103_0420'),
        ('invoice', '0007_auto_20180116_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The universally unique identifier for this model instance.', verbose_name='UUID')),
                ('numbering_scheme', models.CharField(choices=[('%Y-%m', 'yyyy-mm (2018-01)'), ('{number}', '{number} (42, for the 42nd invoice)'), ('%Y-%m-{number}', 'yyyy-mm-{number} (2018-01-42, for the 42nd invoice)'), ('OC-%Y-%m', 'OC-yyyy-mm (OC-2018-01)'), ('OC-{number}', 'OC-{number} (OC-42, for the 42nd invoice)')], default='%Y-%m', help_text='The numbering scheme used to determine how to increment the invoice number.', max_length=80)),
                ('extra_text', models.TextField(blank=True, help_text='Any arbitrary extra text that the provider would like to display on their invoice. Each template should have a designated location to place this extra text.', null=True)),
                ('extra_image', models.ImageField(blank=True, help_text="Any arbitrary extra image that the provider would like to display on their invoice. For example, this could be the provider's signature.", null=True, upload_to='')),
                ('html_template', models.CharField(choices=[('default', 'Default')], default='default', help_text='The template to use to generate an invoice.', max_length=80)),
                ('provider', models.OneToOneField(help_text='The invoicing service/product provider.', on_delete=django.db.models.deletion.CASCADE, related_name='invoice_template', to='account.Account')),
            ],
            options={
                'verbose_name': 'Invoice Template',
                'verbose_name_plural': 'Invoice Templates',
            },
            bases=(accounting.common.mixins.ValidateModelMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='historicalinvoice',
            name='template',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='template',
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='template',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                    to='invoice.InvoiceTemplate'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='template',
            field=models.ForeignKey(help_text='The template to use to generate an invoice.', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, related_name='invoices',
                                    to='invoice.InvoiceTemplate'),
        ),
        # Custom migration code to run after the InvoiceTemplate has been created and the template field is altered.
        migrations.RunPython(
            create_invoice_templates,
            reverse_code=lambda apps, schema_editor: None
        ),
        migrations.RemoveField(
            model_name='historicalinvoice',
            name='extra_image',
        ),
        migrations.RemoveField(
            model_name='historicalinvoice',
            name='extra_text',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='extra_image',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='extra_text',
        ),
    ]
