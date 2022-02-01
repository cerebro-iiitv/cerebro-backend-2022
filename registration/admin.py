from django.contrib import admin
from registration.models import TeamParticipation, TeamMember, IndividualParticipation


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "event",
        "team",
        "registration_data"
    )
    raw_id_fields = (
        "account",
        "event",
        "team",
    )
    search_fields = (
        "event__title",
        "team__team_code",
        "account__user__email",
    )


class TeamParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "team_name",
        "team_captain",
        "current_size",
        "is_full",
        "team_code",
        "submission_data"
    )
    raw_id_fields = ("event",)
    search_fields = (
        "event__title",
        "team_code",
    )
   

class IndividualParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "account",
        "registration_data",
        "submission_data"
    )
    raw_id_fields = (
        "account",
        "event"
    )
    search_fields = (
        "event__title",
    )


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamParticipation, TeamParticipationAdmin)
admin.site.register(IndividualParticipation, IndividualParticipationAdmin)