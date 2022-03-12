from django.db import router
from django.template import base
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from registration.views import (
    IndividualRegistrationViewSet,
    ParticipationDetails,
    TeamRegistrationViewSet,
    SubmissionViewset,
    TeamMemberViewSet
)

router = SimpleRouter()
router.register("individual-registration", IndividualRegistrationViewSet, basename="api-individual-registration")
router.register("team", TeamRegistrationViewSet, basename="api-create-team")
router.register("teammember", TeamMemberViewSet, basename="api-team-member")
# from registration.views import TeamRegistrationViewSet, CsvGenerate, TeamData, index

# router = SimpleRouter()
# router.register("team-register", TeamRegistrationViewSet, basename="api-team")

urlpatterns = [
    path("submission/", SubmissionViewset.as_view(), name="submission"),
    path("excelgenerate/<str:event>", ParticipationDetails.as_view(), name="excel-generate"),
]

# urlpatterns = [
#     path("", index, name="index"),
#     path("csv-generate/<int:pk>", CsvGenerate.as_view(), name="csv-generate"),
#     path("teamdata/", TeamData.as_view(), name="csv-allteam"),
# ]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls

# urlpatterns = []