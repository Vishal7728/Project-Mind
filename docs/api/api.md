# Project Mind API Documentation

## Overview

Project Mind provides a RESTful API for interacting with the AI companion system.

## Endpoints

### GET /api/v1/status

Returns the current status of the AI system.

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "uptime": "2 days, 5 hours, 30 minutes"
}
```

### POST /api/v1/chat

Send a message to the AI companion.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking.",
  "emotion": "happy",
  "timestamp": "2025-12-09T21:00:00Z"
}
```

### GET /api/v1/memory

Retrieve the AI's memory state.

**Response:**
```json
{
  "short_term": {...},
  "long_term": {...}
}
```

## Authentication

All API requests require an API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limiting

The API is rate-limited to 100 requests per hour per API key.

## Error Handling

All errors follow the standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error