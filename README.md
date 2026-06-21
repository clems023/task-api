# django-api

API REST minimaliste de gestion de tâches, construite avec Django et Django REST Framework.

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

## Tester l'API

```bash
curl http://localhost:8000/api/health/
curl http://localhost:8000/api/tasks/
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Ma première tâche"}'
```

## Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/api/health/` | Health check |
| `GET` | `/api/tasks/` | Liste paginée des tâches |
| `POST` | `/api/tasks/` | Créer une tâche |
| `GET` | `/api/tasks/{id}/` | Détail d'une tâche |
| `PATCH` | `/api/tasks/{id}/` | Mise à jour partielle |
| `DELETE` | `/api/tasks/{id}/` | Suppression |

## Tests

```bash
docker compose run web python manage.py test
```

## Structure du projet

```
django-api/
├── config/           # Configuration Django
├── api/              # Application REST (modèles, vues, serializers)
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```
