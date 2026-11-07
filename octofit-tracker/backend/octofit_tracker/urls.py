from django.urls import path

from .views import (
    activities,
    api_root,
    health,
    leaderboard,
    teams,
    users,
    workout_suggestions,
    workouts,
)


urlpatterns = [
    path("", api_root, name="api_root"),
    path("health", health, name="health"),
    path("api/", api_root, name="api"),
    path("api/users", users, name="users"),
    path("api/teams", teams, name="teams"),
    path("api/activities", activities, name="activities"),
    path("api/leaderboard", leaderboard, name="leaderboard"),
    path("api/workouts", workouts, name="workouts"),
    path(
        "api/workouts/suggestions/<str:user_email>",
        workout_suggestions,
        name="workout_suggestions",
    ),
]
