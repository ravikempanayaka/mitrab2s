# Generated by Django 3.0.8 on 2020-07-22 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mitrab2s_app', '0004_auto_20200722_1413'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choice',
            new_name='Answer',
        ),
        migrations.AlterModelTable(
            name='answer',
            table='answer',
        ),
    ]
