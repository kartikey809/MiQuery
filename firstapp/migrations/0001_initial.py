# Generated by Django 4.2.5 on 2023-09-09 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('usecase', models.CharField(max_length=100)),
                ('upvote', models.BigIntegerField(default=0)),
                ('uploadedon', models.DateField(default=datetime.datetime(2023, 9, 9, 21, 12, 1, 454594, tzinfo=datetime.timezone.utc))),
            ],
        ),
    ]
