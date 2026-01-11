# Book Review Platform – Backend

This is the **backend service** for the Book Review Platform, built with **Flask**, **PostgreSQL**, and **SQLAlchemy**, featuring **JWT authentication with access & refresh tokens**, **role-based access control**, **OCI Object Storage integration**, and **modular route architecture**.

The backend is designed to be **Dockerized**, **Kubernetes-ready (K0s)**, and **production-grade**.

---

##  Features

* JWT Authentication (Access + Refresh tokens)
* Admin & User role-based authorization
* Modular Flask blueprint architecture
* PostgreSQL with SQLAlchemy ORM
* OCI Object Storage for book images (0..N images per book)
* Secure password hashing
* Token refresh, logout, logout-all support
* Clean separation of concerns (routes, services, utils)
* Docker & Kubernetes friendly

---

## Project Structure

```
backend/
├── app.py                  # Flask app entrypoint & blueprint registration
├── db.py                   # Database engine & session management
├── models.py               # SQLAlchemy ORM models
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── test.py                 # Local testing / experiments
├── env/                    # Environment files (local development only)
│   └── .env
│
├── routes/                 # API routes (Flask Blueprints)
│   ├── auth.py             # Auth: login, refresh, logout
│   ├── admin_users.py      # Admin user management
│   ├── books.py            # Books CRUD
│   ├── book_authors.py     # Authors CRUD
│   ├── book_genres.py      # Genres CRUD
│   ├── book_reviews.py     # Reviews CRUD
│   ├── book_images.py      # OCI image upload for books
│   └── __init__.py
│
├── services/               # External service integrations
│   ├── oci_storage.py      # OCI Object Storage client & helpers
│   └── __init__.py
│
├── utils/                  # Shared utilities
│   ├── auth_utils.py       # JWT helpers & decorators
│   └── __init__.py
│
└── __pycache__/
```

---

##  Tech Stack

* **Python**
* **Flask**
* **SQLAlchemy**
* **PostgreSQL**
* **JWT (PyJWT)**
* **OCI Object Storage**
* **Docker**
* **Kubernetes (K0s)**

---

##  Authentication Overview

### Token Types

* **Access Token**

  * Short-lived (default: 15 minutes)
  * Used for API authorization
* **Refresh Token**

  * Long-lived (default: 7 days)
  * Stored in DB (hashed)
  * Supports rotation & revocation

### Headers

```http
Authorization: Bearer <access_token>
```

---

##  API Routes

###  Auth

| Method | Endpoint           | Description            |
| ------ | ------------------ | ---------------------- |
| POST   | `/auth/login`      | Login & get tokens     |
| POST   | `/auth/refresh`    | Rotate refresh token   |
| POST   | `/auth/logout`     | Logout current session |
| POST   | `/auth/logout-all` | Logout all sessions    |

---

### Admin Users

| Method | Endpoint            | Description |
| ------ | ------------------- | ----------- |
| POST   | `/admin/users`      | Create user |
| GET    | `/admin/users`      | List users  |
| DELETE | `/admin/users/{id}` | Delete user |

---

###  Authors

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | `/authors`                |
| GET    | `/authors/{id}`           |
| POST   | `/authors` *(admin)*      |
| DELETE | `/authors/{id}` *(admin)* |

---

### Genres

| Method | Endpoint                 |
| ------ | ------------------------ |
| GET    | `/genres`                |
| POST   | `/genres` *(admin)*      |
| DELETE | `/genres/{id}` *(admin)* |

---

### Books

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | `/books`                |
| GET    | `/books/{id}`           |
| POST   | `/books` *(admin)*      |
| DELETE | `/books/{id}` *(admin)* |

---

### Reviews

| Method | Endpoint        |
| ------ | --------------- |
| GET    | `/reviews`      |
| GET    | `/reviews/{id}` |
| POST   | `/reviews`      |
| PUT    | `/reviews/{id}` |
| DELETE | `/reviews/{id}` |

---

### Book Images (OCI)

| Method | Endpoint             | Description        |
| ------ | -------------------- | ------------------ |
| POST   | `/books/{id}/images` | Upload 0..N images |

---

### Health

| Method | Endpoint  |
| ------ | --------- |
| GET    | `/health` |

### User 
| Method | Endpoint            |
| ------ | ------------------- |
| POST   | `/suggestions`      |
| GET    | `/suggestions/mine` |

### Admin
| Method | Endpoint                            |
| ------ | ----------------------------------- |
| GET    | `/admin/suggestions?status=PENDING` |
| POST   | `/admin/suggestions/{id}/approve`   |
| POST   | `/admin/suggestions/{id}/reject`    |

---

## Environment Variables

### JWT

```env
JWT_SECRET=your-secure-secret
ACCESS_TOKEN_MINUTES=15
REFRESH_TOKEN_DAYS=7
```

> In production, inject via **Kubernetes Secrets or OCI Vault**, not `.env`.

---

### Database

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```
---

### OCI Object Storage

```env
OCI_TENANCY_OCID=
OCI_USER_OCID=
OCI_FINGERPRINT=
OCI_PRIVATE_KEY_PATH=
OCI_REGION=

OCI_BUCKET_NAME=book-images
OCI_NAMESPACE=your_namespace
```

---

##  Run Locally (Docker)

```bash
docker build -t book-review-backend .
docker run -p 8000:8000 --env-file env/.env book-review-backend
```

---

##  Run Locally (Without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export JWT_SECRET="dev-secret"
export DATABASE_URL="postgresql://..."

python app.py
```

API available at:

```
http://localhost:8000
```

---


##  Database Migrations (Alembic)

This backend uses **Alembic** to manage database schema migrations.

All migration logic and documentation lives in:

```text
backend/alembic/
````

### Quick Commands

```bash
# Create migration after model changes
alembic revision --autogenerate -m "message"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Multiple Heads?

If you see an error about multiple heads:

```bash
alembic merge heads -m "merge migration heads"
alembic upgrade head
```
 For full details, see
[`backend/alembic/README.md`](./alembic/README.md)

---
## Kubernetes Notes (K0s)

* Backend is **stateless**
* JWT secret injected via Kubernetes Secret
* OCI private key mounted as secret volume
* PostgreSQL deployed separately or managed

---

## Security Best Practices Used

* Password hashing (Werkzeug)
* JWT token type separation
* Refresh token hashing in DB
* Refresh token rotation
* Admin-only endpoints
* No credentials committed to git

---

## Future Improvements

* Alembic migrations
* Swagger / OpenAPI UI
* Rate limiting
* Redis caching
* CI/CD pipeline
* Image CDN (OCI + CDN)
* Full RBAC permissions matrix

---

## License

MIT License – free to use, modify, and distribute.

---
