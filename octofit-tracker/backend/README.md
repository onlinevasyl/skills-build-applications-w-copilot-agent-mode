# OctoFit Django backend

Install the Python dependencies from the repository root and start the Django
development server on the API port. Django MongoDB Backend connects to
`mongodb://localhost:27017` and uses the `octofit_db` database by default.
Set `MONGODB_URI` and `MONGODB_NAME` to override those defaults, and set
`CORS_ALLOWED_ORIGINS` to a comma-separated list when the frontend is not
running at the local Vite origins.

```bash
python -m pip install -r ../../requirements.txt
python manage.py migrate
python manage.py seed_octofit
python manage.py runserver 8000
```

The API root is available at `/` and `/api/`; health is available at
`/health`. The API supports users, teams, activities, leaderboard results, and
workouts under `/api/`. The `seed_octofit` command creates or updates stable
demo teams, users, activities, and workouts without clearing other records;
it is safe to run more than once. Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG`
through the environment before deploying. Models are registered in `admin.py`,
but the admin site is not enabled because this app does not add authentication.

Run the backend checks and tests with:

```bash
python manage.py check
python manage.py test
```
