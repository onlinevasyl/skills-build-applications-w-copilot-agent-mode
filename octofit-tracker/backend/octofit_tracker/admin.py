from django.contrib import admin

from .models import Activity, Team, User, Workout


admin.site.register((User, Team, Activity, Workout))
