# Generated by Django 2.1.5 on 2019-05-02 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webVotingApp', '0011_auto_20190501_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('test_int', models.IntegerField()),
                ('test_char', models.CharField(max_length=1000)),
            ],
        ),
    ]
