# Generated by Django 4.1.5 on 2023-03-10 03:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0003_alter_votings_finish_alter_votings_start"),
    ]

    operations = [
        migrations.AlterField(
            model_name="votings",
            name="finish",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 10, 5, 37, 5, 364964)
            ),
        ),
        migrations.AlterField(
            model_name="votings",
            name="start",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 10, 5, 37, 5, 364964)
            ),
        ),
    ]