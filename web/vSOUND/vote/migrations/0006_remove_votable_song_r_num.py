# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 19:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_votable_song_r_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votable_song',
            name='r_num',
        ),
    ]
