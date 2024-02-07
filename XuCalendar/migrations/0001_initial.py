# Generated by Django 4.1 on 2024-02-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinal', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('week_day', models.IntegerField()),
                ('color', models.CharField(max_length=16)),
                ('special', models.CharField(max_length=128)),
            ],
        ),
    ]