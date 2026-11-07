from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mascot = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        db_column="team",
    )
    fitness_goal = models.CharField(
        max_length=100, blank=True, db_column="fitnessGoal"
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activities", db_column="user"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="activities", db_column="team"
    )
    type = models.CharField(max_length=50)
    minutes = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    occurred_at = models.DateTimeField(db_column="occurredAt")

    class Meta:
        db_table = "activities"


class Workout(models.Model):
    title = models.CharField(max_length=150, unique=True)
    focus = models.CharField(max_length=100)
    minutes = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=50)

    class Meta:
        db_table = "workouts"

    def __str__(self):
        return self.title
