# Chat API

A real time chat API with WebSocket support, file uploads and message history and testcases.

## Getting Started

**Install dependencies**
pip install -r requirements.txt

**Run the server**
uvicorn main:app --reload

**Test the endpoints**
Visit http://127.0.0.1:8000/docs

**Run tests**
pytest test_chat.py -v

## Endpoints

| Method | Endpoint         | Description               |
| ------ | ---------------- | ------------------------- |
| WS     | /chat/{username} | Connect to real time chat |
| GET    | /messages        | Get all chat history      |
| POST   | /uploadfile      | Upload PDF                |

## Tech Stack

- FastAPI
- SQLite
- SQLAlchemy
- WebSockets
- Pytest
