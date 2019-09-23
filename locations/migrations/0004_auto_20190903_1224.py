# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-03 11:24
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations
from django.utils.timezone import make_aware, now


def update_location_create_timestamps(apps, schema_editor):
    Location = apps.get_model('locations', 'Location')
    rcs = Location.objects.filter(type__name='RC')
    for rc in rcs:
        earliest_br_report = rc.birthregistration_records.order_by(
            'time').first()
        if earliest_br_report:
            rc.created = earliest_br_report.time
        else:
            rc.created = now()
        rc.save(update_fields=['created'])

    other_locations = Location.objects.exclude(type__name='RC')
    other_locations.update(created=make_aware(datetime(2011, 1, 28)))


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20190903_1221'),
    ]

    operations = [
        migrations.RunPython(
            update_location_create_timestamps,
            reverse_code=migrations.RunPython.noop
        )
    ]
