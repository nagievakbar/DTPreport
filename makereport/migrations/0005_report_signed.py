# Generated by Django 3.1.5 on 2021-03-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makereport', '0004_auto_20210309_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='signed',
            field=models.BooleanField(default=False),
        ),
    ]
