# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151031_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='subject',
            field=models.IntegerField(default=0, choices=[(0, b'Miscellaneous'), (1, b'Clubs and Activities'), (2, b'Nightlife'), (3, b'Athletics'), (4, b'Res Life'), (5, b'Academics')]),
        ),
    ]
