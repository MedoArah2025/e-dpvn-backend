# syntax=docker/dockerfile:1

FROM python:3.10-slim

# 1) Variables d’env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2) Dépendances système
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 3) Copier requirements & installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copier le code
COPY . .

# 5) Collectstatic si besoin (désactivé en dev)
# RUN python manage.py collectstatic --noinput

# 6) Exposer le port
EXPOSE 8000

# 7) Commande de lancement
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
