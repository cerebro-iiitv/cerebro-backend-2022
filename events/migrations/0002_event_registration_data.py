# Generated by Django 4.0.1 on 2022-01-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
