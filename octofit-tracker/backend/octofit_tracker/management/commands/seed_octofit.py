from datetime import datetime, timezone

from django.core.management.base import BaseCommand

from octofit_tracker.models import Activity, Team, User, Workout


class Command(BaseCommand):
    help = "Create or update the stable OctoFit demo teams, users, activities, and workouts."

    def handle(self, *args, **options):
        octocats, _ = Team.objects.update_or_create(
            name="Octocats", defaults={"mascot": "Mona"}
        )
        robocats, _ = Team.objects.update_or_create(
            name="Robocats", defaults={"mascot": "Hubot"}
        )
        mona, _ = User.objects.update_or_create(
            email="mona@example.com",
            defaults={
                "name": "Mona",
                "team": octocats,
                "fitness_goal": "endurance",
            },
        )
        hubot, _ = User.objects.update_or_create(
            email="hubot@example.com",
            defaults={
                "name": "Hubot",
                "team": robocats,
                "fitness_goal": "strength",
            },
        )

        activities = [
            {
                "user": mona,
                "team": octocats,
                "type": "run",
                "occurred_at": datetime(2026, 1, 10, 12, tzinfo=timezone.utc),
                "minutes": 40,
                "points": 40,
            },
            {
                "user": hubot,
                "team": robocats,
                "type": "cycle",
                "occurred_at": datetime(2026, 1, 11, 12, tzinfo=timezone.utc),
                "minutes": 25,
                "points": 25,
            },
        ]
        for activity in activities:
            identity = {
                key: activity[key]
                for key in ("user", "team", "type", "occurred_at")
            }
            Activity.objects.update_or_create(**identity, defaults=activity)

        for workout in (
            {
                "title": "Intervals",
                "focus": "endurance",
                "minutes": 30,
                "difficulty": "moderate",
            },
            {
                "title": "Strength Circuit",
                "focus": "strength",
                "minutes": 30,
                "difficulty": "moderate",
            },
        ):
            Workout.objects.update_or_create(
                title=workout["title"], defaults=workout
            )

        self.stdout.write(self.style.SUCCESS("OctoFit demo data is ready."))
