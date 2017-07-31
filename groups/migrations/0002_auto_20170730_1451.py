# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 18:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupadultmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups_groupadultmember_related', related_query_name='groups_groupadultmembers', to='groups.Group'),
        ),
        migrations.AlterField(
            model_name='groupchildmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups_groupchildmember_related', related_query_name='groups_groupchildmembers', to='groups.Group'),
        ),
    ]