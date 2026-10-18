# Social Media API

A REST API for a social media application built with Django and Django REST Framework.

## Features

- User registration and token authentication
- User profiles and profile search
- Follow and unfollow users
- Followers and following lists
- Create, retrieve, update, and delete posts
- Personalized feed with posts from followed users
- Permission checks for protected operations

## Tech Stack

- Python 3.11
- Django
- Django REST Framework
- Token Authentication
- SQLite (default Django development database)

## Installation

Clone the repository:

```bash
git clone https://github.com/andriikinash127/py-Social-Media-API.git
cd py-Social-Media-API
```

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

Interactive API documentation is available through Swagger UI:

- Swagger UI: http://127.0.0.1:8000/api/docs/
- OpenAPI schema: http://127.0.0.1:8000/api/schema/

Start the development server before opening the documentation:

```bash
python manage.py runserver
```

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/register/` | Register a user |
| POST | `/api/users/login/` | Log in and obtain a token |
| POST | `/api/users/logout/` | Log out and invalidate the token |

### Profiles and Users

| Method | Endpoint | Description |
|---|---|---|
| GET, PUT, PATCH | `/api/users/me/` | Retrieve or update your profile |
| GET | `/api/users/profiles/<username>/` | Retrieve a public profile |
| GET | `/api/users/search/?search=<query>` | Search users by username |
| POST, DELETE | `/api/users/follow/<username>/` | Follow or unfollow a user |
| GET | `/api/users/following/` | List users you follow |
| GET | `/api/users/followers/` | List your followers |

### Posts

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `/api/posts/` | List posts or create a post |
| GET | `/api/posts/<id>/` | Retrieve a post |
| PUT, PATCH | `/api/posts/<id>/` | Update a post |
| DELETE | `/api/posts/<id>/` | Delete a post |
| GET | `/api/posts/feed/` | Retrieve your feed |

## Authentication

For protected endpoints, include your token in the request header:

```http
Authorization: Token your_token_here
```

## Running Tests

Run the automated test suite:

```bash
python manage.py test
```

Check the Django configuration:

```bash
python manage.py check
```

Check for missing model migrations:

```bash
python manage.py makemigrations --check --dry-run
```

## License

No license specified yet.
