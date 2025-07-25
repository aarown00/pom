# Generated by Django 5.2.4 on 2025-07-24 20:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0019_alter_dailyworkstatus_itinenary_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkstatus',
            name='itinenary_remarks',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkstatus',
            name='time_total',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
