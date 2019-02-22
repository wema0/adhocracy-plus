# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('meinberlin_budgeting', '0018_add_label_verbose_name')]

    dependencies = [
        ('liqd_product_budgeting', '0017_proposal_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='labels',
            field=models.ManyToManyField(related_name='liqd_product_budgeting_proposal_label', to='a4labels.Label', verbose_name='Labels'),
        ),
    ]
