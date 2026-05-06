# Regression Based Ride Prediction

Simple Django web app for Uber ride fare prediction using a trained regression model.

## Stack

- Django
- scikit-learn
- pandas
- matplotlib
- Docker
- Render

## Features

- User registration and login
- Admin and user dashboards
- Dataset view
- Model training
- Fare prediction

## Local Run

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Docker Run

Build the image:

```bash
docker build -t regression-ride-prediction .
```

Run the container:

```bash
docker run -p 8000:8000 regression-ride-prediction
```

Open:

```text
http://127.0.0.1:8000/
```

## Render Deployment

This project is set up for a simple Docker deployment on Render free tier.

Behavior:

- no persistent disk
- SQLite is packaged with the app
- files created at runtime are temporary
- each restart or redeploy behaves like a fresh site

### Required Environment Variables

Set these in Render:

```env
DJANGO_SECRET_KEY=<your-random-secret-key>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=.onrender.com
```

### Optional for Custom Domain

Only add this if you connect your own domain:

```env
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com
DJANGO_ALLOWED_HOSTS=.onrender.com,yourdomain.com
```

### Do Not Set Manually

Render provides these automatically:

- `PORT`
- `RENDER_EXTERNAL_HOSTNAME`

## Render Config

The project includes:

- `Dockerfile`
- `start.sh`
- `render.yaml`

`start.sh` runs:

- `python manage.py migrate --noinput`
- `python manage.py collectstatic --noinput`
- `gunicorn Uber_fare.wsgi:application`

## Notes

- Keep `db.sqlite3` tracked if you want starter data bundled into deployment.
- Keep model files in `media/` tracked if prediction should work immediately after deploy.
- Runtime-generated files are not persistent on Render free tier.
