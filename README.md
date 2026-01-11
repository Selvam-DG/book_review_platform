#  Book Review Platform

A full-stack, containerized **Book Review Platform** built with **Flask**, **PostgreSQL**, and a modern **Vite (TypeScript + Tailwind CSS)** frontend.
The application is fully Dockerized and deployed on a **K0s Kubernetes cluster**, with images hosted on **Docker Hub**.

This project demonstrates clean backend architecture, RESTful API design, authentication & authorization, relational data modeling, and real-world container orchestration.

---

##  Features

###  Authentication & Authorization

* JWT-based authentication
* Role-based access control (Admin vs User)
* Secure password hashing (Werkzeug)
* Token expiration handling

###  User Management

* User registration & login
* Admin-only user creation, listing, and deletion
* Admin role enforcement across protected routes

###  Books & Metadata

* CRUD operations for:

  * Authors
  * Genres
  * Books
* Strong relational modeling using SQLAlchemy
* Automatic cascading deletes for related entities

###  Reviews System

* Users can review books (1–5 rating)
* One review per user per book (DB-level constraint)
* Admin override permissions
* Helpful count tracking

###  Backend Architecture

* Flask REST API
* SQLAlchemy ORM (PostgreSQL)
* Clean separation of concerns:

  * Models
  * Database session management
  * Authentication helpers
* Centralized error handling
* Health check endpoint

###  Frontend

* Vite
* TypeScript
* Tailwind CSS
* Consumes backend REST API

###  DevOps & Deployment

* Dockerized backend and frontend
* Images pushed to Docker Hub
* Kubernetes deployment using **K0s**
* Stateless API pods
* Environment-based configuration

---

##  Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy
* PostgreSQL
* JWT (PyJWT)
* Werkzeug Security
* Flask-CORS

### Frontend

* Vite
* TypeScript
* Tailwind CSS

### Infrastructure

* Docker
* Docker Hub
* Kubernetes (K0s)
* PostgreSQL (containerized or managed)

---

##  System Architecture

```
┌────────────┐     ┌──────────────┐
│  Frontend  │ ──▶ │  Flask API   │
│  (Vite)    │     │  (JWT Auth)  │
└────────────┘     └──────┬───────┘
                           │
                     ┌─────▼─────┐
                     │ PostgreSQL│
                     └───────────┘

Docker Images → Docker Hub → K0s Kubernetes Cluster
```

---

##  Database Design

### Core Entities

* **User**
* **Author**
* **Genre**
* **Book**
* **Review**

### Key Relationships

* Author → Books (1-to-many)
* Genre → Books (1-to-many)
* Book → Reviews (1-to-many)
* User → Reviews (1-to-many)
* Unique constraint: **(book_id, user_id)** in reviews

---

##  API Overview

### Authentication

* `POST /auth/register`
* `POST /auth/login`

### Admin

* `POST /admin/users`
* `GET /admin/users`
* `DELETE /admin/users/{id}`

### Authors

* `GET /authors`
* `GET /authors/{id}`
* `POST /authors` *(Admin only)*
* `DELETE /authors/{id}` *(Admin only)*

### Genres

* `GET /genres`
* `POST /genres` *(Admin only)*
* `DELETE /genres/{id}` *(Admin only)*

### Books

* `GET /books`
* `GET /books/{id}`
* `POST /books` *(Admin only)*
* `DELETE /books/{id}` *(Admin only)*

### Reviews

* `GET /reviews`
* `GET /reviews/{id}`
* `POST /reviews` *(Authenticated users)*
* `PUT /reviews/{id}`
* `DELETE /reviews/{id}`

### Health Check

* `GET /health`

---

##  Environment Variables

Backend requires the following environment variables:

```env
SECRET_KEY=your_jwt_secret
DATABASE_URL=postgresql://user:password@host:port/dbname
PORT=8000
```

---

## Running Locally with Docker

```bash
docker build -t book-review-backend .
docker run -p 8000:8000 --env-file .env book-review-backend
```

---

##  Kubernetes Deployment (K0s)

* Docker images are pushed to Docker Hub
* Kubernetes pulls images directly from Docker Hub
* Stateless Flask API pods
* PostgreSQL deployed separately or externally

Example:

```bash
kubectl apply -f k8s/
```

---

##  Health Check

```bash
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

##  Future Improvements

* Pagination & filtering
* Search (title, author, genre)
* Rate limiting
* API documentation (OpenAPI / Swagger)
* CI/CD pipeline
* Helm charts
* Caching (Redis)
* Full RBAC with permissions matrix

---

##  License

This project is open-source and available under the **MIT License**.

---

