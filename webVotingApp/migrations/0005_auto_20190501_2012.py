# Generated by Django 2.1.5 on 2019-05-01 20:12

from django.db import migrations, models
import webVotingApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webVotingApp', '0004_dummy_author_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='year_name',
            field=models.IntegerField(unique=True, validators=[webVotingApp.models.year_validation]),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('author_first_name', 'author_last_name')},
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('author', 'year')},
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together={('year', 'member')},
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('judge', 'candidate')},
        ),
    ]