# Generated by Django 4.0.1 on 2022-02-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]