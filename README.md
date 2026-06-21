# task-api

API REST de gestion de tâches, construite avec Django et Django REST Framework. Authentification JWT, CI GitHub Actions, page d'accueil animée.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Démarrage rapide

```bash
git clone https://github.com/clems023/task-api.git
cd task-api
cp .env.example .env
docker compose up --build
```

L'API est disponible sur [http://localhost:8000](http://localhost:8000).

## Authentification (JWT)

Les endpoints `/api/tasks/` nécessitent un token Bearer.

```bash
# 1. Créer un compte
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "securepass123"}'

# 2. Obtenir un token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "securepass123"}'

# 3. Utiliser le token (remplacer <access>)
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <access>"

curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access>" \
  -d '{"title": "Ma première tâche"}'
```

Rafraîchir le token :

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh>"}'
```

## Endpoints

| Méthode | Route | Auth | Description |
|---------|-------|------|-------------|
| `GET` | `/api/health/` | Non | Health check |
| `POST` | `/api/auth/register/` | Non | Inscription |
| `POST` | `/api/auth/token/` | Non | Obtenir access + refresh |
| `POST` | `/api/auth/token/refresh/` | Non | Rafraîchir le token |
| `GET` | `/api/tasks/` | Oui | Liste paginée (ses tâches) |
| `POST` | `/api/tasks/` | Oui | Créer une tâche |
| `GET` | `/api/tasks/{id}/` | Oui | Détail |
| `PATCH` | `/api/tasks/{id}/` | Oui | Mise à jour partielle |
| `DELETE` | `/api/tasks/{id}/` | Oui | Suppression |

## Tests & qualité

```bash
# Tests
docker compose run web python manage.py test

# Lint local (optionnel)
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
```

## CI

Chaque push/PR sur `main` déclenche :

- **Lint** — Ruff (style + format)
- **Tests** — suite Django
- **Docker** — build de l'image + tests en conteneur

## Structure du projet

```
task-api/
├── .github/workflows/ci.yml
├── config/              # Configuration Django
├── api/                 # Application REST
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml       # Config Ruff
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```
