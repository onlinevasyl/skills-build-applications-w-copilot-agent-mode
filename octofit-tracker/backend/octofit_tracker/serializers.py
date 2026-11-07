import json

from bson import ObjectId
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class InputError(ValueError):
    pass


def parse_payload(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise InputError("Request body must contain valid JSON.") from error
    if not isinstance(payload, dict):
        raise InputError("Request body must be a JSON object.")
    return payload


def required_string(payload, name):
    value = payload.get(name)
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{name} must be a non-empty string.")
    return value.strip()


def positive_integer(payload, name):
    value = payload.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise InputError(f"{name} must be a positive integer.")
    return value


def object_id(value, name):
    if not isinstance(value, str) or not ObjectId.is_valid(value):
        raise InputError(f"{name} must be a valid ID.")
    return ObjectId(value)


def serialize_team(team):
    return {
        "id": str(team.pk),
        "name": team.name,
        "mascot": team.mascot,
        "members": [str(member.pk) for member in team.members.all()],
    }


def serialize_user(user):
    return {
        "id": str(user.pk),
        "name": user.name,
        "email": user.email,
        "team": str(user.team_id) if user.team_id else None,
        "fitnessGoal": user.fitness_goal,
    }


def serialize_activity(activity):
    return {
        "id": str(activity.pk),
        "user": str(activity.user_id),
        "team": str(activity.team_id),
        "type": activity.type,
        "minutes": activity.minutes,
        "points": activity.points,
        "occurredAt": activity.occurred_at.isoformat(),
    }


def serialize_workout(workout):
    return {
        "id": str(workout.pk),
        "title": workout.title,
        "focus": workout.focus,
        "minutes": workout.minutes,
        "difficulty": workout.difficulty,
    }


def validate_email_address(value):
    try:
        validate_email(value)
    except ValidationError as error:
        raise InputError("email must be a valid email address.") from error
    return value
