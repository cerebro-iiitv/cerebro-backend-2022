# Generated by Django 4.0.1 on 2022-01-27 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_is_closed_event_registration_closed_and_more'),
        ('accounts', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='registration_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TeamParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_size', models.IntegerField(default=1)),
                ('is_full', models.BooleanField(default=False)),
                ('team_code', models.CharField(default=None, max_length=15)),
                ('registration_data', models.JSONField(blank=True, null=True)),
                ('submission_data', models.JSONField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_team', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_data', models.JSONField(blank=True, null=True)),
                ('submission_data', models.JSONField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_user', to='accounts.account')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_individual', to='events.event')),
            ],
        ),
        migrations.AlterField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_member', to='registration.teamparticipation'),
        ),
        migrations.DeleteModel(
            name='TeamStatus',
        ),
    ]
