# Generated by Django 3.1.5 on 2021-03-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makereport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='pdf_qr_code',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]