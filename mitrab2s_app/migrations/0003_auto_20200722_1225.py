# Generated by Django 3.0.8 on 2020-07-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitrab2s_app', '0002_auto_20200722_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]