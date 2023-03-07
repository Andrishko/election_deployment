# Generated by Django 4.1.5 on 2023-03-07 00:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0011_alter_votings_finish_alter_votings_start_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="votings",
            name="finish",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 7, 2, 20, 17, 665597)
            ),
        ),
        migrations.AlterField(
            model_name="votings",
            name="start",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 7, 2, 20, 17, 665597)
            ),
        ),
        migrations.AlterField(
            model_name="votingtime",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 7, 2, 20, 17, 666597)
            ),
        ),
    ]
