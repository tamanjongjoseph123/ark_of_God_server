# Courses API - Complete Documentation

## Overview

The Courses API provides a hierarchical content management system for educational materials:
- **Courses** → **Modules** → **Course Videos** → **Comments**

Two course categories are available:
- `sons_of_john_chi`
- `mentorship`

## Table of Contents
1. [Authentication](#authentication)
2. [Courses](#courses)
3. [Modules](#modules)
4. [Course Videos](#course-videos)
5. [Comments](#comments)
6. [Complete Workflow Examples](#complete-workflow-examples)

---

## Authentication

### Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Permission**: AllowAny

**Request:**
```json
{
  "username": "admin",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "country": "USA",
    "contact": "+1234567890"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

Save the `token` value:
```bash
export TOKEN="your_access_token_here"
```

### Refresh Token
- **URL**: `/api/token/refresh`
- **Method**: `POST`

**Request:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_access_token"
}
```

---

## Courses

### List All Courses
- **URL**: `/api/courses/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `category` (optional): Filter by `sons_of_john_chi` or `mentorship`

**cURL Example:**
```bash
# Get all courses
curl http://localhost:8000/api/courses/

# Filter by category
curl http://localhost:8000/api/courses/?category=sons_of_john_chi
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Foundations of Faith",
    "description": "Introduction to core principles",
    "category": "sons_of_john_chi",
    "image": "https://example.com/media/courses/foundations.jpg",
    "created_at": "2025-11-07T00:00:00Z"
  }
]
```

### Create a Course
- **URL**: `/api/courses/`
- **Method**: `POST`
- **Permission**: IsAdminUser (requires `is_staff=True`)
- **Content-Type**: `multipart/form-data`

**Fields:**
- `name` (required): string
- `description` (required): string
- `category` (required): `sons_of_john_chi` | `mentorship`
- `image` (required): file upload

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer $TOKEN" \
  -F name="Foundations of Faith" \
  -F description="Introduction to core principles" \
  -F category="sons_of_john_chi" \
  -F image=@/path/to/course-image.jpg
```

### Get Single Course
- **URL**: `/api/courses/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**cURL Example:**
```bash
curl http://localhost:8000/api/courses/1/
```

### Update a Course
- **URL**: `/api/courses/{id}/`
- **Methods**: `PUT` (full update), `PATCH` (partial update)
- **Permission**: IsAdminUser

**cURL Example (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/courses/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F description="Updated description"
```

### Delete a Course
- **URL**: `/api/courses/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/courses/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Modules

### List All Modules
- **URL**: `/api/modules/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `course` (optional): Filter by course ID

**cURL Example:**
```bash
# Get all modules
curl http://localhost:8000/api/modules/

# Filter by course
curl http://localhost:8000/api/modules/?course=1
```

**Response:**
```json
[
  {
    "id": 1,
    "course": 1,
    "name": "Module 1: Basics",
    "description": "Introduction to the fundamentals",
    "image": "https://example.com/media/modules/module1.jpg",
    "created_at": "2025-11-07T00:00:00Z"
  }
]
```

### Create a Module
- **URL**: `/api/modules/`
- **Method**: `POST`
- **Permission**: IsAdminUser
- **Content-Type**: `multipart/form-data`

**Fields:**
- `course` (required): integer (Course ID)
- `name` (required): string
- `description` (required): string
- `image` (required): file upload

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/modules/ \
  -H "Authorization: Bearer $TOKEN" \
  -F course=1 \
  -F name="Module 1: Basics" \
  -F description="Introduction to the fundamentals" \
  -F image=@/path/to/module-image.jpg
```

### Get Single Module
- **URL**: `/api/modules/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**cURL Example:**
```bash
curl http://localhost:8000/api/modules/1/
```

### Update a Module
- **URL**: `/api/modules/{id}/`
- **Methods**: `PUT`, `PATCH`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X PATCH http://localhost:8000/api/modules/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F name="Module 1: Updated Title"
```

### Delete a Module
- **URL**: `/api/modules/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/modules/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Course Videos

### List All Course Videos
- **URL**: `/api/course-videos/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `module` (optional): Filter by module ID

**cURL Example:**
```bash
# Get all videos
curl http://localhost:8000/api/course-videos/

# Filter by module
curl http://localhost:8000/api/course-videos/?module=1
```

**Response:**
```json
[
  {
    "id": 1,
    "module": 1,
    "name": "Lesson 1: Introduction",
    "description": "Welcome to the course",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "key_takeaways": "1. Main concept\n2. Secondary point\n3. Action items",
    "assignments": "Complete worksheet 1 and submit by Friday",
    "created_at": "2025-11-07T00:00:00Z"
  }
]
```

### Create a Course Video
- **URL**: `/api/course-videos/`
- **Method**: `POST`
- **Permission**: IsAdminUser
- **Content-Type**: `application/json`

**Fields:**
- `module` (required): integer (Module ID)
- `name` (required): string
- `description` (required): string
- `youtube_url` (required): string (YouTube URL)
- `key_takeaways` (optional): string (multiline text)
- `assignments` (optional): string (multiline text)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/course-videos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module": 1,
    "name": "Lesson 1: Introduction",
    "description": "Welcome to the course",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "key_takeaways": "1. Understand the basics\n2. Learn key concepts\n3. Practice daily",
    "assignments": "Watch the video twice and take notes"
  }'
```

### Get Single Course Video
- **URL**: `/api/course-videos/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**cURL Example:**
```bash
curl http://localhost:8000/api/course-videos/1/
```

### Update a Course Video
- **URL**: `/api/course-videos/{id}/`
- **Methods**: `PUT`, `PATCH`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X PATCH http://localhost:8000/api/course-videos/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key_takeaways": "Updated key points",
    "assignments": "New assignment details"
  }'
```

### Delete a Course Video
- **URL**: `/api/course-videos/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/course-videos/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Comments

### List Comments for a Video
- **URL**: `/api/comments/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `video` (optional): Filter by video ID

**cURL Example:**
```bash
# Get all comments
curl http://localhost:8000/api/comments/

# Get comments for specific video
curl http://localhost:8000/api/comments/?video=1
```

**Response (with nested replies):**
```json
[
  {
    "id": 1,
    "video": 1,
    "user": {
      "id": 2,
      "username": "john_doe",
      "email": "john@example.com",
      "country": "USA",
      "contact": "+1234567890"
    },
    "parent": null,
    "text": "Great lesson! Very clear explanation.",
    "created_at": "2025-11-07T01:00:00Z",
    "replies": [
      {
        "id": 2,
        "video": 1,
        "user": {
          "id": 3,
          "username": "jane_smith",
          "email": "jane@example.com",
          "country": "Canada",
          "contact": "+9876543210"
        },
        "parent": 1,
        "text": "I agree! This helped me understand the concept.",
        "created_at": "2025-11-07T01:05:00Z",
        "replies": []
      }
    ]
  }
]
```

### Create a Comment (Top-level)
- **URL**: `/api/comments/`
- **Method**: `POST`
- **Permission**: IsAuthenticated
- **Content-Type**: `application/json`

**Fields:**
- `video` (required): integer (Video ID)
- `parent` (optional): integer (Parent comment ID, null for top-level)
- `text` (required): string

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 1,
    "parent": null,
    "text": "This is an excellent video! Thank you for sharing."
  }'
```

### Reply to a Comment
- **URL**: `/api/comments/`
- **Method**: `POST`
- **Permission**: IsAuthenticated

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 1,
    "parent": 1,
    "text": "Thanks for your feedback! Glad it helped."
  }'
```

### Get Single Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**cURL Example:**
```bash
curl http://localhost:8000/api/comments/1/
```

### Update a Comment
- **URL**: `/api/comments/{id}/`
- **Methods**: `PUT`, `PATCH`
- **Permission**: IsAuthenticated (owner)

**cURL Example:**
```bash
curl -X PATCH http://localhost:8000/api/comments/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated comment text"
  }'
```

### Delete a Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAuthenticated (owner)

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/comments/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Complete Workflow Examples

### Scenario 1: Admin Creates Complete Course Structure

```bash
# Step 1: Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Save the token
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Step 2: Create a course
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer $TOKEN" \
  -F name="Spiritual Growth Journey" \
  -F description="A comprehensive guide to spiritual development" \
  -F category="sons_of_john_chi" \
  -F image=@course-cover.jpg

# Response: {"id": 1, ...}

# Step 3: Create modules under the course
curl -X POST http://localhost:8000/api/modules/ \
  -H "Authorization: Bearer $TOKEN" \
  -F course=1 \
  -F name="Module 1: Foundation" \
  -F description="Building a strong spiritual foundation" \
  -F image=@module1.jpg

# Response: {"id": 1, ...}

curl -X POST http://localhost:8000/api/modules/ \
  -H "Authorization: Bearer $TOKEN" \
  -F course=1 \
  -F name="Module 2: Growth" \
  -F description="Developing your spiritual gifts" \
  -F image=@module2.jpg

# Response: {"id": 2, ...}

# Step 4: Add videos to Module 1
curl -X POST http://localhost:8000/api/course-videos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module": 1,
    "name": "Lesson 1: Prayer Basics",
    "description": "Learn the fundamentals of effective prayer",
    "youtube_url": "https://www.youtube.com/watch?v=example1",
    "key_takeaways": "1. Prayer is conversation with God\n2. Be honest and authentic\n3. Listen as much as you speak",
    "assignments": "Practice praying for 10 minutes daily this week"
  }'

# Response: {"id": 1, ...}

curl -X POST http://localhost:8000/api/course-videos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module": 1,
    "name": "Lesson 2: Scripture Reading",
    "description": "How to read and understand the Bible",
    "youtube_url": "https://www.youtube.com/watch?v=example2",
    "key_takeaways": "1. Start with the Gospels\n2. Read in context\n3. Apply what you learn",
    "assignments": "Read one chapter daily and journal your insights"
  }'

# Response: {"id": 2, ...}
```

### Scenario 2: User Views Course and Engages

```bash
# Step 1: User logs in
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"pass123"}'

export TOKEN="user_token_here"

# Step 2: Browse courses by category
curl http://localhost:8000/api/courses/?category=sons_of_john_chi

# Step 3: View modules for a course
curl http://localhost:8000/api/modules/?course=1

# Step 4: View videos for a module
curl http://localhost:8000/api/course-videos/?module=1

# Step 5: Get specific video details
curl http://localhost:8000/api/course-videos/1/

# Step 6: View comments on the video
curl http://localhost:8000/api/comments/?video=1

# Step 7: Post a comment
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 1,
    "parent": null,
    "text": "This lesson really helped me understand prayer better!"
  }'

# Step 8: Reply to another user's comment
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video": 1,
    "parent": 5,
    "text": "I had the same experience! Keep practicing."
  }'
```

### Scenario 3: Admin Updates Course Content

```bash
# Update course description
curl -X PATCH http://localhost:8000/api/courses/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F description="Updated: A comprehensive 12-week guide to spiritual development"

# Update video with new assignments
curl -X PATCH http://localhost:8000/api/course-videos/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignments": "Week 1: Practice praying for 10 minutes daily\nWeek 2: Increase to 15 minutes and journal your prayers"
  }'

# Add key takeaways to existing video
curl -X PATCH http://localhost:8000/api/course-videos/2/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key_takeaways": "1. Context is crucial\n2. Use study tools\n3. Pray before reading\n4. Apply to your life"
  }'
```

---

## Permissions Summary

| Endpoint | GET | POST | PUT/PATCH | DELETE |
|----------|-----|------|-----------|--------|
| `/api/courses/` | Public | Admin | Admin | Admin |
| `/api/modules/` | Public | Admin | Admin | Admin |
| `/api/course-videos/` | Public | Admin | Admin | Admin |
| `/api/comments/` | Public | Authenticated | Authenticated | Authenticated |

**Admin** = User with `is_staff=True`  
**Authenticated** = Any logged-in user  
**Public** = No authentication required

---

## Data Hierarchy

```
Course (category: sons_of_john_chi | mentorship)
  ├── Module 1
  │   ├── Video 1 (with key_takeaways, assignments)
  │   │   ├── Comment 1
  │   │   │   └── Reply 1
  │   │   │       └── Reply 2
  │   │   └── Comment 2
  │   └── Video 2
  └── Module 2
      └── Video 3
```

---

## Error Handling

### Common Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

**400 Bad Request:**
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

---

## Best Practices

1. **Always authenticate admin requests** with `Authorization: Bearer <token>`
2. **Use multipart/form-data** for image uploads (courses, modules)
3. **Use application/json** for video and comment creation
4. **Filter results** using query parameters to reduce payload size
5. **Handle nested replies** recursively in your frontend
6. **Validate YouTube URLs** before submission
7. **Store tokens securely** and refresh before expiration
8. **Check permissions** before attempting write operations

---

## Migration Required

After implementing this API, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the necessary database tables for courses, modules, videos, and comments.
