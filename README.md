# URL Shortener - Midterm Project

**Software Engineering Course - AUT**  
**Date: December 2025**

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Setup & Installation](#setup--installation)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Team Members](#team-members)

---

## Introduction

This project is a **URL Shortener** backend system implemented as part of the Software Engineering midterm exam. The system allows users to shorten long URLs into compact, shareable links that redirect to the original URLs.

## Project Overview

The URL Shortener service receives a long internet address and provides a short, usable address in return. When users visit the short URL, they are automatically redirected to the original URL. This type of system is commonly used for link sharing, traffic management, and visitor analytics.

### Key Features

- ✅ Create shortened URLs with unique codes
- ✅ Redirect to original URLs
- ✅ Retrieve all shortened URLs
- ✅ Get URL metadata by short code
- ✅ Delete shortened URLs
- ✅ RESTful API design
- ✅ Comprehensive error handling
- ✅ Input validation with Pydantic
- ✅ Database migrations with Alembic

---

## Architecture

The project follows a **layered architecture** with clear separation of concerns:

```
Controller (Router) → Service → Repository → Model
```

### Layers

1. **Controller/Router Layer** (`api/controllers/`)
   - Handles HTTP requests and responses
   - Defines API endpoints
   - Validates input using Pydantic schemas

2. **Service Layer** (`core/services/`)
   - Contains business logic
   - URL validation
   - Short code generation
   - Coordinates between controllers and repositories

3. **Repository Layer** (`data/repositories/`)
   - Database operations
   - Data access abstraction
   - Implements repository interface

4. **Model Layer** (`core/models/`)
   - SQLAlchemy models
   - Database table definitions

### Dependency Injection

The project uses **Constructor Injection** for dependency management:

- Controllers depend on Services (injected via FastAPI `Depends`)
- Services depend on Repositories (injected via constructor)
- No layer directly instantiates lower layers
- This ensures loose coupling and high testability

### Repository Pattern

- **Interface**: `core/repositories/url_repository.py` (IUrlRepository)
- **Implementation**: `data/repositories/Sql_url_repository.py` (SqlUrlRepository)
- Services depend on the interface, not the concrete implementation

---

## Technology Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI 0.115.0
- **ORM**: SQLAlchemy 2.0.23
- **Database**: PostgreSQL
- **Migrations**: Alembic 1.13.1
- **Dependency Management**: Poetry
- **Validation**: Pydantic 2.12.5
- **API Testing**: Postman

---

## Setup & Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Poetry (for dependency management)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd URL-Shortener
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DB_USER=your_db_user
   DB_PASS=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=url_shortener
   ```
   
   Or use a full DATABASE_URL:
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   poetry run python -m api.main
   ```
   
   Or using uvicorn directly:
   ```bash
   poetry run uvicorn api.main:app --reload
   ```

6. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs (Swagger): `http://localhost:8000/docs`
   - Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Create Short URL
**POST** `/urls`

Creates a new shortened URL.

**Request Body:**
```json
{
  "original_url": "https://example.com"
}
```

**Success Response (201):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "original_url": "https://example.com",
    "short_code": "abc123",
    "created_at": "2025-12-12T20:00:00Z"
  }
}
```

**Error Response (400):**
```json
{
  "status": "failure",
  "message": "Invalid URL"
}
```

---

#### 2. Get All URLs
**GET** `/urls`

Retrieves all shortened URLs.

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "original_url": "https://example.com",
      "short_code": "abc123",
      "created_at": "2025-12-12T20:00:00Z"
    }
  ]
}
```

---

#### 3. Get URL Metadata
**GET** `/urls/{short_code}`

Retrieves metadata for a specific short code.

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "original_url": "https://example.com",
    "short_code": "abc123",
    "created_at": "2025-12-12T20:00:00Z"
  }
}
```

**Error Response (404):**
```json
{
  "status": "failure",
  "message": "URL not found"
}
```

---

#### 4. Redirect to Original URL
**GET** `/urls/u/{short_code}`

Redirects to the original URL (HTTP 302).

**Query Parameters:**
- `json` (optional, boolean): If `true`, returns JSON instead of redirecting (useful for API testing)

**Success Response (302):**
- Redirects to the original URL
- Location header contains the original URL

**Error Response (404):**
```json
{
  "status": "failure",
  "message": "URL not found"
}
```

---

#### 5. Delete URL
**DELETE** `/urls/{short_code}`

Deletes a shortened URL.

**Success Response (204):**
- No content (empty body)

**Error Response (404):**
```json
{
  "status": "failure",
  "message": "URL not found"
}
```

---

## Project Structure

```
URL-Shortener/
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py              # Alembic configuration
├── api/                     # API layer
│   ├── controllers/        # Route handlers
│   │   └── url_controller.py
│   ├── controller_schemas/ # Pydantic schemas
│   │   └── url_schemas.py
│   └── main.py             # FastAPI application
├── config/                  # Configuration
│   └── settings.py         # Environment settings
├── core/                    # Core business logic
│   ├── models/             # SQLAlchemy models
│   │   └── url_model.py
│   ├── repositories/        # Repository interfaces
│   │   └── url_repository.py
│   └── services/           # Business logic
│       └── url_service.py
├── data/                    # Data access layer
│   ├── db/                 # Database setup
│   │   ├── session.py      # Session management
│   │   └── sql_db_base.py  # SQLAlchemy Base
│   └── repositories/       # Repository implementations
│       └── Sql_url_repository.py
├── alembic.ini             # Alembic configuration
├── pyproject.toml          # Poetry dependencies
└── README.md               # This file
```

---

## Testing

### API Test Coverage Table

| # | API Endpoint / Feature | Implemented & Tested By (Student Name) |
|---|------------------------|----------------------------------------|
| 1 | Create Short Link - **POST /urls** | Sam Ghorbani-40212038 |
| 2 | Redirect to Original URL - **GET /urls/u/{short_code}** | Nima Sayad-40213017 |
| 3 | Get All Shortened Links - **GET /urls** | Sam Ghorbani-40212038 |
| 4 | Get URL Metadata - **GET /urls/{short_code}** | Nima Sayad-40213017 |
| 5 | Delete Short Link - **DELETE /urls/{short_code}** | Nima Sayad-40213017 |

---

## Code Generation Method

The short code is generated using:

- [x] **1. Random Generation** ✅
- [ ] **2. ID → Base62 Conversion**
- [ ] **3. Hash-based Generation**

**Implementation Details:**
- Method: Random 6-character string using Base62 characters (A-Z, a-z, 0-9)
- Location: `core/services/url_service.py` → `_generate_short_code()`
- Uniqueness: Checks database for collisions and retries up to 10 times

---

## Bonus User Story: TTL (Expiration Time) for Shortened Links

- [ ] **TTL Feature Implemented**

**If checked, fill in the following information:**

- **ENV variable or config key used:**
  ```
  (Not implemented)
  ```

- **Location of TTL Logic (File + Function):**
  ```
  (Not implemented)
  ```

- **How TTL cleanup is triggered:**
  ```
  (Not implemented)
  ```

---

## Postman Collection

A **Postman Collection** has been created and includes all API routes:

- ✅ **POST /urls** - Create short URL
- ✅ **GET /urls/u/{short_code}** - Redirect to original URL
- ✅ **GET /urls** - Get all URLs
- ✅ **GET /urls/{short_code}** - Get URL metadata
- ✅ **DELETE /urls/{short_code}** - Delete URL

### Screenshots

Screenshots for each route (success and error responses) are located in:
```
/postman/
```

### Naming Convention

Screenshots follow this naming pattern:
- `post-urls-201-success.png`
- `post-urls-400-invalid-url.png`
- `get-urls-200-success.png`
- `get-urls-404-not-found.png`
- `get-u-{code}-302-redirect.png`
- `get-u-{code}-404-not-found.png`
- `delete-urls-204-success.png`
- `delete-urls-404-not-found.png`

**Filenames clearly show:**
- Route (HTTP method + path)
- HTTP status code
- Success or error type

---

## Team Members

- **Sam Ghorbani** (40212038)
  - Portfolio: [https://sami-gh05.github.io/personal-portfolio-website/](https://sami-gh05.github.io/personal-portfolio-website/)

- **Nima Sayad** (40213017)

---

## Development Guidelines

### RESTful Naming Conventions

- ✅ Uses plural nouns for routes (`/urls` not `/url`)
- ✅ Uses HTTP verbs for operations (POST, GET, DELETE)
- ✅ No verbs in route paths
- ✅ Consistent response format with `status` and `data` fields

### Code Quality

- ✅ Type hints throughout the codebase
- ✅ Input validation with Pydantic
- ✅ Comprehensive error handling
- ✅ PEP8 compliant naming conventions
- ✅ Proper HTTP status codes

### Database

- ✅ PostgreSQL database
- ✅ Alembic for migrations
- ✅ SQLAlchemy ORM
- ✅ Proper indexing on `short_code` for performance

---

## License

This project is part of the Software Engineering course midterm exam at AUT.

---

## Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Alembic documentation
- Software Engineering Course - AUT
