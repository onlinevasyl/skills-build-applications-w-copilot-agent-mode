---
description: "Update the OctoFit Django app to use MongoDB and expose its API"
agent: "agent"
model: "GPT-4.1"
---

# Django App Updates

Update the OctoFit Django application. All Django project and app files for
this task are in `octofit-tracker/backend/octofit_tracker`.

1. Update `settings.py` to connect to the MongoDB database `octofit_db` on port
   `27017` and configure CORS for the Vite frontend on port `5173`. Use a
   supported Django/MongoDB integration and document any required environment
   variables or dependencies. Do not expose secrets in source code.
2. Update `models.py`, `serializers.py`, `urls.py`, `views.py`, `tests.py`, and
   `admin.py` to support the users, teams, activities, leaderboard, and
   workouts collections and their API behavior.
3. Ensure `/` points to the API and `api_root` is present in `urls.py`.
4. Preserve the existing API contracts and project constraints: the API runs
   on port `8000`, the frontend on `5173`, MongoDB on `27017`, and do not add
   authentication.
5. Add or update tests for the API behavior and invalid inputs. Run Django
   checks and tests, and report the commands and results.
