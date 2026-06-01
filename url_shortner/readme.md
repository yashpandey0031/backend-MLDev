# URL Shortener API

A simple URL shortener built with FastAPI and PostgreSQL.

## Getting Started

**Install dependencies**
pip install -r requirements.txt

**Run the server**
uvicorn main:app --reload

**Test the endpoints**
Visit http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint | Description                              |
| ------ | -------- | ---------------------------------------- |
| POST   | /shorten | Submit a long URL, get a short code back |
| GET    | /{code}  | Redirects to the original URL            |

## Tech Stack

- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy

## Live API

https://your-render-url.onrender.com/docs
