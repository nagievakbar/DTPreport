# Generated by Django 3.1.5 on 2021-03-27 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('makereport', '0002_calculation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', to='makereport.report', verbose_name='Репорт'),
        ),
    ]