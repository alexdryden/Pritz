# Generated by Django 2.1.5 on 2019-05-01 20:48

from django.db import migrations, models
import webVotingApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webVotingApp', '0008_auto_20190501_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='year_name',
            field=models.IntegerField(default=2020, unique=True, validators=[
                webVotingApp.models.year_validation]),
        ),
    ]
