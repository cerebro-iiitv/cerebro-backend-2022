# Generated by Django 4.0.2 on 2022-02-28 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=100)),
                ('starts_on', models.DateTimeField()),
                ('action', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=52)),
                ('current_size', models.IntegerField(default=1)),
                ('is_full', models.BooleanField(default=False)),
                ('team_code', models.CharField(default=None, max_length=15)),
                ('submission_data', models.JSONField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_team', to='events.event')),
                ('team_captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_creator_acc', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_data', models.JSONField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_team', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='events.event')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_member', to='registration.teamparticipation')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_data', models.JSONField(blank=True, null=True)),
                ('submission_data', models.JSONField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_user', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_individual', to='events.event')),
            ],
        ),
    ]
