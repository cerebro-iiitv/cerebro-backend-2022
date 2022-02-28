from django.core.management.base import BaseCommand
from events.models import Event

class Command(BaseCommand):
    help = "To populate event"

    def handle(self, *args, **options):
        Event.objects.create(
            priority = 1,
            event_type = "tech",
            team_event = True,
            short_name = "tech",
            description = "Tech hunt",
            title = "Tech Hunt",
            prize = "INR 10,000",
            team_size = 2,
            start_time = "18-03-2022 18:00",
            end_time = "19-03-2022 23:59"
        )