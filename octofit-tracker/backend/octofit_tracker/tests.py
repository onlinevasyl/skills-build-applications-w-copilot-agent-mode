from datetime import datetime, timezone

from django.core.management import call_command
from django.test import TestCase

from .models import Activity, Team, User, Workout


class OctoFitApiTests(TestCase):
    def setUp(self):
        self.octocats = Team.objects.create(name="Octocats", mascot="Mona")
        self.robocats = Team.objects.create(name="Robocats", mascot="Hubot")
        self.mona = User.objects.create(
            name="Mona",
            email="mona@example.com",
            team=self.octocats,
            fitness_goal="endurance",
        )
        self.hubot = User.objects.create(
            name="Hubot",
            email="hubot@example.com",
            team=self.robocats,
            fitness_goal="strength",
        )

    def test_api_root_and_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["activities"], "/api/activities")

        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True})

    def test_team_and_user_endpoints(self):
        response = self.client.get("/api/teams")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["teams"]), 2)

        invalid = self.client.post(
            "/api/teams", data={"mascot": "Mona"}, content_type="application/json"
        )
        self.assertEqual(invalid.status_code, 400)

        created_team = self.client.post(
            "/api/teams",
            data={"name": "New Team", "mascot": "Octo", "members": [str(self.mona.pk)]},
            content_type="application/json",
        )
        self.assertEqual(created_team.status_code, 201)
        self.mona.refresh_from_db()
        self.assertEqual(self.mona.team.name, "New Team")

        created_user = self.client.post(
            "/api/users",
            data={"name": "New User", "email": "new@example.com"},
            content_type="application/json",
        )
        self.assertEqual(created_user.status_code, 201)
        self.assertEqual(len(self.client.get("/api/users").json()["users"]), 3)

    def test_activity_validation_listing_and_leaderboard(self):
        invalid = self.client.post(
            "/api/activities",
            data={"userId": "invalid", "teamId": str(self.octocats.pk), "type": "run", "minutes": 30},
            content_type="application/json",
        )
        self.assertEqual(invalid.status_code, 400)

        created = self.client.post(
            "/api/activities",
            data={
                "userId": str(self.mona.pk),
                "teamId": str(self.octocats.pk),
                "type": "run",
                "minutes": 30,
            },
            content_type="application/json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["activity"]["points"], 30)
        self.assertEqual(len(self.client.get("/api/activities").json()["activities"]), 1)

        Activity.objects.create(
            user=self.hubot,
            team=self.robocats,
            type="cycle",
            minutes=50,
            points=50,
            occurred_at=datetime.now(timezone.utc),
        )
        leaderboard = self.client.get("/api/leaderboard").json()["leaderboard"]
        self.assertEqual(
            [(entry["teamName"], entry["totalPoints"], entry["rank"]) for entry in leaderboard],
            [("Robocats", 50, 1), ("Octocats", 30, 2)],
        )

    def test_workout_suggestions_and_cors(self):
        Workout.objects.create(
            title="Intervals", focus="endurance", minutes=30, difficulty="moderate"
        )
        Workout.objects.create(
            title="Strength Circuit", focus="strength", minutes=30, difficulty="moderate"
        )

        response = self.client.get("/api/workouts/suggestions/mona%40example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["suggestions"][0]["focus"], "endurance")
        self.assertIn("reason", response.json()["suggestions"][0])

        missing_user = self.client.get(
            "/api/workouts/suggestions/nobody%40example.com"
        )
        self.assertEqual(missing_user.status_code, 404)

        cors = self.client.options(
            "/api/teams", HTTP_ORIGIN="http://localhost:5173"
        )
        self.assertEqual(cors["Access-Control-Allow-Origin"], "http://localhost:5173")


class OctoFitSeedTests(TestCase):
    def test_seed_is_repeatable_and_populates_demo_records(self):
        call_command("seed_octofit")
        call_command("seed_octofit")

        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Activity.objects.count(), 2)
        self.assertEqual(Workout.objects.count(), 2)
        self.assertEqual(
            User.objects.get(email="mona@example.com").team.name, "Octocats"
        )
        self.assertEqual(
            User.objects.get(email="hubot@example.com").team.name, "Robocats"
        )
