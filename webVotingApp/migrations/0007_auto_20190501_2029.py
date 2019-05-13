# Generated by Django 2.1.5 on 2019-05-01 20:29

from django.db import migrations, models
import webVotingApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webVotingApp', '0006_auto_20190501_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='year_name',
            field=models.IntegerField(default=2019, max_length=4, unique=True, validators=[
                webVotingApp.models.year_validation]),
        ),
    ]
