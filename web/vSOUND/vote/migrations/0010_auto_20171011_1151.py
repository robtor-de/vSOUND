# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0009_auto_20171011_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suspended_song',
            name='song_album',
        ),
        migrations.RemoveField(
            model_name='votable_song',
            name='song_album',
        ),
    ]
