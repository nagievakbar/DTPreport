# Generated by Django 3.1.5 on 2021-01-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makereport', '0010_auto_20210125_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='key',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]