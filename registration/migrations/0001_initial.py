# Generated by Django 4.0.1 on 2022-01-25 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('events', '0001_initial'),
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
            name='TeamStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_size', models.IntegerField(default=1)),
                ('is_full', models.BooleanField(default=False)),
                ('team_code', models.CharField(default=None, max_length=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_team', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_team', to='accounts.account')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='events.event')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_member', to='registration.teamstatus')),
            ],
        ),
    ]