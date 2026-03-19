# 🍽️ Recipe API

A production-ready RESTful API for managing recipes, built with Django REST Framework using Test-Driven Development (TDD), Docker, PostgreSQL, Swagger documentation, and CI integration.

---

## 🚀 Project Overview

Recipe API is a fully containerized backend service that allows authenticated users to:

- Manage recipes (CRUD)
- Create and assign tags
- Create and assign ingredients
- Upload recipe images
- Filter recipes by tags & ingredients
- Authenticate securely using token-based authentication

The project follows clean architecture principles and is structured for scalability and maintainability.

---

## 🧰 Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Test-Driven Development (TDD)**
- **Swagger / OpenAPI (drf-spectacular)**
- **GitHub Actions (CI Pipeline)**
- **Flake8 (Linting)**
- **Vercel (Deployment)**

---

## 🏗️ Architecture Overview

The project follows a modular architecture:

```
app/
├── app/            # Django project configuration
│   ├── settings/   # base, dev, prod settings
│   ├── urls.py
│   └── wsgi.py
├── core/           # Custom user model & shared models
├── users/          # User & authentication APIs
├── recipe/         # Recipe, Tags, Ingredients APIs
└── manage.py
```

### Key Architectural Decisions

- Custom User Model
- Environment-based settings (base/dev/prod)
- App-level separation of concerns
- Docker-first development
- Command-based DB readiness (`wait_for_db`)
- User data isolation (multi-user secure design)

---

## 🔐 Authentication

- Token-based authentication
- Secure endpoints for authenticated users only
- Each user only accesses their own data

---

## 📚 API Features

### 👤 Users API
- Create user
- Generate authentication token
- Retrieve & update authenticated user profile

---

### 🍲 Recipes API
- Create recipe
- Retrieve recipe list
- Retrieve recipe detail
- Update recipe
- Delete recipe
- Filter recipes by:
  - Tags
  - Ingredients
- Upload recipe image

---

### 🥕 Ingredients API
- Create ingredient
- List ingredients
- Update ingredient
- Filter assigned-only ingredients

---

### 🏷️ Tags API
- Create tag
- List tags
- Update tag
- Filter assigned-only tags

---

## 📖 API Documentation

Postman Documentation:

[https://documenter.getpostman.com/view/29368996/2sBXihrDKh](https://documenter.getpostman.com/view/29368996/2sBXihrDKh)

Swagger UI:

```
/api/docs/
```
Redoc UI:

```
/api/redoc/
```

Generated using `drf-spectacular`.

OpenAPI schema:

```
/api/schema/
```

Generated using `drf-spectacular`.

---

## 🌐 Deployment

Live deployment link:  

[https://recipe-api-git-prod-zeyad-salamas-projects.vercel.app/)

---

## 🧪 Testing Strategy (TDD)

The project was developed using Test-Driven Development.

Test Coverage Includes:

- Model tests
- API endpoint tests
- Authentication tests
- Permission tests
- Image upload tests
- Management command tests (`wait_for_db`)
- Admin tests

Run tests:

```bash
make test
```

Or:

```bash
docker-compose run --rm app python manage.py test
```

---

## 🐳 Docker Setup

### Build the project

```bash
make build
```

### Start services

```bash
make up
```

### Stop services

```bash
make down
```

### Rebuild without cache

```bash
make rebuild
```

---

## ⚙️ Development Workflow

### Apply migrations

```bash
make migrate
```

### Create migrations

```bash
make makemigrations
```

### Lint the project

```bash
make lint
```

### Create superuser

```bash
make superuser
```

### Open Django shell

```bash
make django_shell
```

---

## 🗄️ Database

- PostgreSQL (Dockerized)
- Database readiness handled using custom `wait_for_db` management command
- Environment-based configuration

---

## 🔄 CI Pipeline

Automated pipeline runs on:

- Push to `main`
- Pull requests

Pipeline includes:

- Docker build
- Linting
- Running test suite

Ensures production-grade code quality before merge.

---

## 🔥 Production Readiness Features

- Environment-based settings (dev/prod separation)
- Secure file uploads
- Token authentication
- User-level data isolation
- Clean Docker setup
- Linting enforcement
- Automated testing
- CI validation

---

## 📌 Why This Project Matters

This project demonstrates:

- Strong backend engineering fundamentals
- RESTful API design best practices
- Secure authentication handling
- Test-Driven Development workflow
- Docker-based development
- PostgreSQL integration
- CI/CD understanding
- Writing clean, scalable, maintainable backend code

---

## 🧠 Future Improvements

- Add rate limiting
- Add caching layer (Redis)
- Implement background tasks (Celery)
- Add API versioning
- Deploy to cloud provider (AWS / Render / DigitalOcean)

---

## 👨‍💻 Author

**Zeyad**
Backend Developer | Python & Django
