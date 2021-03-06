# Generated by Django 3.0.8 on 2020-07-22 12:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    atomic = False

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.CharField(max_length=50)),
                ('create_program', models.CharField(max_length=200)),
                ('modify_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modify_user', models.CharField(max_length=50)),
                ('modify_program', models.CharField(max_length=200)),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.CharField(max_length=50)),
                ('create_program', models.CharField(max_length=200)),
                ('modify_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modify_user', models.CharField(max_length=50)),
                ('modify_program', models.CharField(max_length=200)),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mitrab2s_app.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
