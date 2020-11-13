# Generated by Django 3.1.2 on 2020-11-13 08:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0010_auto_20201112_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duser',
            name='picture',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='membership',
            name='dateJoined',
            field=models.DateField(default=datetime.date(2020, 11, 13)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.duser'),
        ),
    ]
