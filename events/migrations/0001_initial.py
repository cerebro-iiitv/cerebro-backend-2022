# Generated by Django 4.0.2 on 2022-02-28 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('event_type', models.CharField(choices=[('tech', 'Technical'), ('gaming', 'Gaming'), ('design-photo', 'Design and Photography'), ('lit', 'Literature')], max_length=30)),
                ('team_event', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('short_name', models.CharField(blank=True, max_length=4)),
                ('description', models.TextField(blank=True)),
                ('prize', models.CharField(blank=True, max_length=20)),
                ('team_size', models.IntegerField(default=1)),
                ('start_time', models.CharField(max_length=100)),
                ('end_time', models.CharField(max_length=100)),
                ('rules_doc', models.URLField(blank=True)),
                ('social_media', models.URLField(blank=True, null=True)),
                ('registration_closed', models.BooleanField(default=False)),
                ('registration_attributes', models.JSONField(blank=True, null=True)),
                ('submission_required', models.BooleanField(default=False)),
                ('submission_closed', models.BooleanField(default=False)),
                ('submission_attributes', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('Convenor', 'Convenor'), ('Co-Convenor1', 'Co_Convenor1'), ('Co-Convenor2', 'Co_Convenor2'), ('Member1', 'Member1'), ('Member2', 'Member2')], max_length=15)),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.event')),
            ],
        ),
    ]
