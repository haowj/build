# Generated by Django 2.0.2 on 2019-04-02 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_strategyrecord_deviceid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategyrecord',
            name='deviceID',
        ),
    ]
