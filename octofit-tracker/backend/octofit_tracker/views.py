from datetime import datetime, timezone

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from .models import Activity, Team, User, Workout
from .serializers import (
    InputError,
    object_id,
    parse_payload,
    positive_integer,
    required_string,
    serialize_activity,
    serialize_team,
    serialize_user,
    serialize_workout,
    validate_email_address,
)


def _input_error(error):
    return JsonResponse({"error": str(error)}, status=400)


def _not_found(message):
    return JsonResponse({"error": message}, status=404)


@require_GET
def api_root(request):
    return JsonResponse(
        {
            "users": "/api/users",
            "teams": "/api/teams",
            "activities": "/api/activities",
            "leaderboard": "/api/leaderboard",
            "workouts": "/api/workouts",
        }
    )


@require_GET
def health(request):
    return JsonResponse({"ok": True})


@require_http_methods(["GET", "POST"])
def users(request):
    if request.method == "GET":
        return JsonResponse(
            {"users": [serialize_user(user) for user in User.objects.all()]}
        )

    try:
        payload = parse_payload(request)
        name = required_string(payload, "name")
        email = validate_email_address(required_string(payload, "email"))
        fitness_goal = payload.get("fitnessGoal", "")
        if not isinstance(fitness_goal, str):
            raise InputError("fitnessGoal must be a string.")
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "A user with this email already exists."}, status=409)

        team = None
        if payload.get("team") is not None:
            team_pk = object_id(payload["team"], "team")
            try:
                team = Team.objects.get(pk=team_pk)
            except Team.DoesNotExist:
                return _not_found("Team not found.")

        user = User.objects.create(
            name=name, email=email, team=team, fitness_goal=fitness_goal.strip()
        )
        return JsonResponse({"user": serialize_user(user)}, status=201)
    except InputError as error:
        return _input_error(error)


@require_http_methods(["GET", "POST"])
def teams(request):
    if request.method == "GET":
        return JsonResponse(
            {"teams": [serialize_team(team) for team in Team.objects.all()]}
        )

    try:
        payload = parse_payload(request)
        name = required_string(payload, "name")
        mascot = payload.get("mascot", "")
        if not isinstance(mascot, str):
            raise InputError("mascot must be a string.")
        member_ids = payload.get("members", [])
        if not isinstance(member_ids, list):
            raise InputError("members must be a list of user IDs.")
        member_pks = [object_id(member_id, "member ID") for member_id in member_ids]
        members = list(User.objects.filter(pk__in=member_pks))
        if len(members) != len(set(member_pks)):
            return _not_found("One or more users were not found.")
        if Team.objects.filter(name=name).exists():
            return JsonResponse({"error": "A team with this name already exists."}, status=409)

        team = Team.objects.create(name=name, mascot=mascot.strip())
        if members:
            User.objects.filter(pk__in=[member.pk for member in members]).update(team=team)
        return JsonResponse({"team": serialize_team(team)}, status=201)
    except InputError as error:
        return _input_error(error)


@require_http_methods(["GET", "POST"])
def activities(request):
    if request.method == "GET":
        return JsonResponse(
            {
                "activities": [
                    serialize_activity(activity) for activity in Activity.objects.all()
                ]
            }
        )

    try:
        payload = parse_payload(request)
        user_pk = object_id(payload.get("userId"), "userId")
        team_pk = object_id(payload.get("teamId"), "teamId")
        activity_type = required_string(payload, "type")
        minutes = positive_integer(payload, "minutes")
        try:
            user = User.objects.get(pk=user_pk)
            team = Team.objects.get(pk=team_pk)
        except User.DoesNotExist:
            return _not_found("User not found.")
        except Team.DoesNotExist:
            return _not_found("Team not found.")

        occurred_at = datetime.now(timezone.utc)
        activity = Activity.objects.create(
            user=user,
            team=team,
            type=activity_type,
            minutes=minutes,
            points=minutes,
            occurred_at=occurred_at,
        )
        return JsonResponse({"activity": serialize_activity(activity)}, status=201)
    except InputError as error:
        return _input_error(error)


@require_GET
def leaderboard(request):
    ranked_teams = []
    for team in Team.objects.all():
        points = sum(team.activities.values_list("points", flat=True))
        ranked_teams.append(
            {"teamName": team.name, "totalPoints": points}
        )
    ranked_teams.sort(key=lambda entry: (-entry["totalPoints"], entry["teamName"]))
    for rank, entry in enumerate(ranked_teams, start=1):
        entry["rank"] = rank
    return JsonResponse({"leaderboard": ranked_teams})


@require_GET
def workouts(request):
    return JsonResponse(
        {"workouts": [serialize_workout(workout) for workout in Workout.objects.all()]}
    )


@require_GET
def workout_suggestions(request, user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return _not_found("User not found.")

    focus = user.fitness_goal
    reason = f"Recommended for your {focus} fitness goal."
    if not focus:
        recent_activity = user.activities.order_by("-occurred_at").first()
        if recent_activity:
            focus = recent_activity.type
            reason = f"Recommended based on your recent {focus} activity."

    suggestions = list(Workout.objects.filter(focus__iexact=focus))
    if not suggestions:
        suggestions = list(Workout.objects.all())
    serialized = [serialize_workout(workout) for workout in suggestions]
    if serialized:
        serialized[0]["reason"] = reason
    return JsonResponse({"suggestions": serialized})
