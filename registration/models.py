from django.db import models

from accounts.models import Account
from events.models import Event


class Dashboard(models.Model):
    event_name = models.CharField(max_length=100, blank=True)
    starts_on = models.DateTimeField()
    action = models.BooleanField(default=True)


class IndividualParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reg_individual")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="reg_user")
    registration_data = models.JSONField(null=True, blank=True)
    submission_data = models.JSONField(null=True, blank=True)


class TeamParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reg_team")
    team_creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="team_creator_acc")
    team_name = models.CharField(max_length=52, blank=False)
    current_size = models.IntegerField(default=1)
    is_full = models.BooleanField(default=False)
    team_code = models.CharField(max_length=15, default=None)
    registration_data = models.JSONField(null=True, blank=True)
    submission_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.team_code


class TeamMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user_team")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="member")
    team = models.ForeignKey(TeamParticipation, on_delete=models.CASCADE, related_name="team_member")
    registration_data = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.event.title + " | " + self.team.team_code
