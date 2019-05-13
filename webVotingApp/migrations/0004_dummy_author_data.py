# Generated by Django 2.1.5 on 2019-03-31 19:49
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations

AUTHORS =[

     ]


def add_author_data(apps, schema_editor):
    author_class = apps.get_model('webVotingApp', 'Author')
    for author in AUTHORS:
        try:
            duplicate_object = author_class.objects.get(
                author_first_name=author['first_name'],
                author_last_name=author['last_name'],
                info_href=author['info_href']
            )
            print('Duplicate author entry not added to author table:',
                  author['first_name'], author['last_name']
                  )
        except ObjectDoesNotExist:
            author_object = author_class.objects.create(
                author_first_name=author['first_name'],
                author_last_name=author['last_name'],
                info_href=author['info_href']
            )


def remove_author_data(apps, schema_editor):
    author_class = apps.get_model('webVotingApp', 'Author')
    for author in AUTHORS:
        author_object = author_class.objects.get(
            author_first_name=author['first_name'],
            author_last_name=author['last_name']
        )
        author_object.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('webVotingApp', '0003_author_info_href'),
    ]

    operations = [migrations.RunPython(
        add_author_data,
        remove_author_data
    )
    ]
