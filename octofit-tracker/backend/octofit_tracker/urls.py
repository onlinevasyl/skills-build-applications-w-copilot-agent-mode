import os

from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET

from .views import (
    activities,
    health,
    leaderboard,
    teams,
    users,
    workout_suggestions,
    workouts,
)


@require_GET
def api_root(request):
    codespace_name = os.environ.get("CODESPACE_NAME")
    base_url = (
        f"https://{codespace_name}-8000.app.github.dev" if codespace_name else ""
    )
    endpoint_suffix = "/" if codespace_name else ""
    return JsonResponse(
        {
            "users": f"{base_url}/api/users{endpoint_suffix}",
            "teams": f"{base_url}/api/teams{endpoint_suffix}",
            "activities": f"{base_url}/api/activities{endpoint_suffix}",
            "leaderboard": f"{base_url}/api/leaderboard{endpoint_suffix}",
            "workouts": f"{base_url}/api/workouts{endpoint_suffix}",
        }
    )


urlpatterns = [
    path("", api_root, name="api_root"),
    path("health", health, name="health"),
    path("api/", api_root, name="api"),
    path("api/users", users, name="users"),
    path("api/users/", users),
    path("api/teams", teams, name="teams"),
    path("api/teams/", teams),
    path("api/activities", activities, name="activities"),
    path("api/activities/", activities),
    path("api/leaderboard", leaderboard, name="leaderboard"),
    path("api/leaderboard/", leaderboard),
    path("api/workouts", workouts, name="workouts"),
    path("api/workouts/", workouts),
    path(
        "api/workouts/suggestions/<str:user_email>",
        workout_suggestions,
        name="workout_suggestions",
    ),
    path("api/workouts/suggestions/<str:user_email>/", workout_suggestions),
]
