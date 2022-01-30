# Generated by Django 4.0.1 on 2022-01-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_rename_registration_data_event_registration_attributes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_closed',
            new_name='registration_closed',
        ),
        migrations.AddField(
            model_name='event',
            name='submission_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='submission_required',
            field=models.BooleanField(default=False),
        ),
    ]
