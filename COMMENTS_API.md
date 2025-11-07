# Comments API Documentation

## Overview

Users can comment on course videos and reply to other comments, creating threaded discussions.

## Models

### CourseVideo (Updated)
- `key_takeaways` (optional): Text field for key learning points
- `assignments` (optional): Text field for homework/tasks

### Comment
- `video`: ForeignKey to CourseVideo
- `user`: ForeignKey to User (auto-assigned on create)
- `parent`: ForeignKey to Comment (null for top-level comments)
- `text`: Comment content
- `created_at`: Timestamp

## Endpoints

### List/Create Comments
- **URL**: `/api/comments/`
- **Methods**: `GET`, `POST`
- **Permission**: GET: AllowAny, POST: IsAuthenticated
- **Query Params (GET)**:
  - `video`: Video ID to filter comments (optional)

### GET Response (Top-level comments with nested replies)
```json
[
  {
    "id": 1,
    "video": 5,
    "user": {
      "id": 2,
      "username": "john_doe",
      "email": "john@example.com",
      "country": "USA",
      "contact": "+1234567890"
    },
    "parent": null,
    "text": "Great lesson!",
    "created_at": "2025-11-07T01:00:00Z",
    "replies": [
      {
        "id": 2,
        "video": 5,
        "user": {
          "id": 3,
          "username": "jane_smith",
          "email": "jane@example.com",
          "country": "Canada",
          "contact": "+9876543210"
        },
        "parent": 1,
        "text": "I agree!",
        "created_at": "2025-11-07T01:05:00Z",
        "replies": []
      }
    ]
  }
]
```

### POST Request Body (Create Comment)
```json
{
  "video": 5,
  "parent": null,
  "text": "This is a top-level comment"
}
```

### POST Request Body (Reply to Comment)
```json
{
  "video": 5,
  "parent": 1,
  "text": "This is a reply to comment #1"
}
```

### Retrieve/Update/Delete Comment
- **URL**: `/api/comments/{id}/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Permission**: GET: AllowAny, Mutations: IsAuthenticated (own comments only recommended)

## Course Video Updates

### Create/Update Course Video (with new fields)
```json
{
  "module": 10,
  "name": "Lesson 1",
  "description": "Introduction to the topic",
  "youtube_url": "https://www.youtube.com/watch?v=...",
  "key_takeaways": "1. Main point one\n2. Main point two\n3. Main point three",
  "assignments": "Complete the worksheet and submit by Friday"
}
```

## Usage Examples (cURL)

### 1. Get all comments for a video
```bash
curl http://localhost:8000/api/comments/?video=5
```

### 2. Post a top-level comment (requires auth)
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 5,
    "parent": null,
    "text": "Great video! Very informative."
  }'
```

### 3. Reply to a comment (requires auth)
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 5,
    "parent": 1,
    "text": "Thanks for sharing your thoughts!"
  }'
```

### 4. Create a course video with key takeaways and assignments
```bash
curl -X POST http://localhost:8000/api/course-videos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module": 10,
    "name": "Advanced Concepts",
    "description": "Deep dive into advanced topics",
    "youtube_url": "https://www.youtube.com/watch?v=example",
    "key_takeaways": "1. Understanding the fundamentals\n2. Practical applications\n3. Common pitfalls to avoid",
    "assignments": "Read chapter 5 and complete exercises 1-10"
  }'
```

## Notes

- Comments are ordered by most recent first (`-created_at`)
- Only top-level comments (parent=null) are returned in list view
- Replies are nested within their parent comments via the `replies` field
- The `user` field is automatically set to the authenticated user on comment creation
- Both `key_takeaways` and `assignments` are optional fields on CourseVideo
- Users must be authenticated to post comments or replies
