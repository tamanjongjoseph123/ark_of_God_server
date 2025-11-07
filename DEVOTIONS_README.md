# Daily Devotions API - Complete Documentation

## Overview

The Daily Devotions API allows admins to upload daily devotional content that users can view on the app. Devotions can be either text-based or video-based (YouTube), providing flexibility in content delivery.

## Features

- **Two Content Types**: Text devotions or YouTube video devotions
- **Daily Schedule**: Each devotion is assigned to a specific date
- **Auto Thumbnails**: YouTube video thumbnails are automatically extracted
- **Today's Devotion**: Special endpoint to fetch the current day's devotion
- **Filtering**: Filter by content type, date, or get today's devotion
- **Admin Only Upload**: Only staff users can create/edit devotions
- **Public Access**: All users can view devotions without authentication

---

## Table of Contents

1. [Authentication](#authentication)
2. [Devotion Model](#devotion-model)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)

---

## Authentication

### Admin Access Required

Only authenticated admin users (with `is_staff=True`) can create, update, or delete devotions.

**Login to get admin token:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

Save the token:
```bash
export TOKEN="your_access_token_here"
```

---

## Devotion Model

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Auto | Unique identifier |
| `title` | String | Yes | Devotion title |
| `content_type` | String | Yes | Either `text` or `video` |
| `description` | Text | Yes | Brief description/summary |
| `text_content` | Text | Conditional | Required if `content_type` is `text` |
| `youtube_url` | URL | Conditional | Required if `content_type` is `video` |
| `devotion_date` | Date | Yes | Date for this devotion (YYYY-MM-DD) |
| `created_at` | DateTime | Auto | Timestamp of creation |
| `thumbnail_url` | String | Read-only | Auto-generated YouTube thumbnail |

### Content Type Rules

- **Text Devotion**: Must provide `text_content`, `youtube_url` is optional/ignored
- **Video Devotion**: Must provide `youtube_url`, `text_content` is optional/ignored
- **Unique Dates**: Only one devotion per date is allowed

---

## API Endpoints

### 1. List All Devotions

- **URL**: `/api/devotions/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `content_type` (optional): Filter by `text` or `video`
  - `date` (optional): Filter by specific date (YYYY-MM-DD)
  - `today` (optional): Set to `true` to get today's devotion

**Examples:**

```bash
# Get all devotions
curl http://localhost:8000/api/devotions/

# Get only text devotions
curl http://localhost:8000/api/devotions/?content_type=text

# Get only video devotions
curl http://localhost:8000/api/devotions/?content_type=video

# Get devotion for specific date
curl http://localhost:8000/api/devotions/?date=2025-11-07

# Get today's devotion
curl http://localhost:8000/api/devotions/?today=true
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Walking in Faith",
    "content_type": "text",
    "description": "Learning to trust God in uncertain times",
    "text_content": "Today we explore what it means to walk by faith...",
    "youtube_url": null,
    "devotion_date": "2025-11-07",
    "created_at": "2025-11-06T10:00:00Z",
    "thumbnail_url": null
  },
  {
    "id": 2,
    "title": "The Power of Prayer",
    "content_type": "video",
    "description": "Understanding effective prayer",
    "text_content": null,
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "devotion_date": "2025-11-08",
    "created_at": "2025-11-06T11:00:00Z",
    "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
]
```

### 2. Get Today's Devotion (Special Endpoint)

- **URL**: `/api/devotions/today/`
- **Method**: `GET`
- **Permission**: AllowAny

**Example:**
```bash
curl http://localhost:8000/api/devotions/today/
```

**Response (if devotion exists for today):**
```json
{
  "id": 5,
  "title": "Grace for Today",
  "content_type": "text",
  "description": "God's sufficient grace for each day",
  "text_content": "His grace is new every morning...",
  "youtube_url": null,
  "devotion_date": "2025-11-07",
  "created_at": "2025-11-07T00:00:00Z",
  "thumbnail_url": null
}
```

**Response (if no devotion for today):**
```json
{
  "detail": "No devotion for today"
}
```
*Status: 404*

### 3. Get Single Devotion

- **URL**: `/api/devotions/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**Example:**
```bash
curl http://localhost:8000/api/devotions/1/
```

### 4. Create a Text Devotion

- **URL**: `/api/devotions/`
- **Method**: `POST`
- **Permission**: IsAdminUser (requires authentication)
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "title": "Walking in Faith",
  "content_type": "text",
  "description": "Learning to trust God in uncertain times",
  "text_content": "Today we explore what it means to walk by faith and not by sight. In times of uncertainty, God calls us to trust Him completely...\n\nKey Points:\n1. Faith is trusting God even when we can't see the outcome\n2. God's promises are always faithful\n3. Our faith grows through testing\n\nPrayer: Lord, help me to trust You more each day. Amen.",
  "devotion_date": "2025-11-07"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/devotions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Walking in Faith",
    "content_type": "text",
    "description": "Learning to trust God in uncertain times",
    "text_content": "Today we explore what it means to walk by faith...",
    "devotion_date": "2025-11-07"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Walking in Faith",
  "content_type": "text",
  "description": "Learning to trust God in uncertain times",
  "text_content": "Today we explore what it means to walk by faith...",
  "youtube_url": null,
  "devotion_date": "2025-11-07",
  "created_at": "2025-11-06T10:00:00Z",
  "thumbnail_url": null
}
```

### 5. Create a Video Devotion

- **URL**: `/api/devotions/`
- **Method**: `POST`
- **Permission**: IsAdminUser
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "title": "The Power of Prayer",
  "content_type": "video",
  "description": "Understanding effective prayer through scripture",
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "devotion_date": "2025-11-08"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/devotions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Power of Prayer",
    "content_type": "video",
    "description": "Understanding effective prayer through scripture",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "devotion_date": "2025-11-08"
  }'
```

**Response:**
```json
{
  "id": 2,
  "title": "The Power of Prayer",
  "content_type": "video",
  "description": "Understanding effective prayer through scripture",
  "text_content": null,
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "devotion_date": "2025-11-08",
  "created_at": "2025-11-06T11:00:00Z",
  "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
}
```

### 6. Update a Devotion

- **URL**: `/api/devotions/{id}/`
- **Methods**: `PUT` (full update), `PATCH` (partial update)
- **Permission**: IsAdminUser

**PATCH Example (partial update):**
```bash
curl -X PATCH http://localhost:8000/api/devotions/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Walking in Faith - Updated",
    "description": "Updated description with more context"
  }'
```

**PUT Example (full update):**
```bash
curl -X PUT http://localhost:8000/api/devotions/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Walking in Faith - Revised",
    "content_type": "text",
    "description": "Completely revised devotion",
    "text_content": "New content here...",
    "devotion_date": "2025-11-07"
  }'
```

### 7. Delete a Devotion

- **URL**: `/api/devotions/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/devotions/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
*Status: 204 No Content*

---

## Usage Examples

### Scenario 1: Admin Creates Weekly Devotions

```bash
# Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

export TOKEN="your_token_here"

# Monday - Text devotion
curl -X POST http://localhost:8000/api/devotions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Monday Motivation",
    "content_type": "text",
    "description": "Starting the week with purpose",
    "text_content": "As we begin this new week, let us remember that God has a purpose for each day...",
    "devotion_date": "2025-11-10"
  }'

# Tuesday - Video devotion
curl -X POST http://localhost:8000/api/devotions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tuesday Teaching",
    "content_type": "video",
    "description": "Deep dive into scripture",
    "youtube_url": "https://www.youtube.com/watch?v=example123",
    "devotion_date": "2025-11-11"
  }'

# Wednesday - Text devotion
curl -X POST http://localhost:8000/api/devotions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Midweek Encouragement",
    "content_type": "text",
    "description": "Finding strength in the middle of the week",
    "text_content": "When we feel weary, God renews our strength...",
    "devotion_date": "2025-11-12"
  }'
```

### Scenario 2: User Views Devotions on Mobile App

```bash
# Get today's devotion (no auth required)
curl http://localhost:8000/api/devotions/today/

# Browse all devotions
curl http://localhost:8000/api/devotions/

# View only video devotions
curl http://localhost:8000/api/devotions/?content_type=video

# Get devotion for specific date
curl http://localhost:8000/api/devotions/?date=2025-11-10

# View specific devotion details
curl http://localhost:8000/api/devotions/5/
```

### Scenario 3: Admin Updates Existing Devotion

```bash
# Fix typo in title
curl -X PATCH http://localhost:8000/api/devotions/5/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Monday Motivation - Corrected Title"
  }'

# Change from text to video
curl -X PUT http://localhost:8000/api/devotions/5/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Monday Motivation",
    "content_type": "video",
    "description": "Starting the week with purpose",
    "youtube_url": "https://www.youtube.com/watch?v=newvideo",
    "devotion_date": "2025-11-10"
  }'
```

---

## Error Handling

### Common Errors

#### 1. Missing Required Content

**Request:**
```json
{
  "title": "Test",
  "content_type": "text",
  "description": "Test devotion",
  "devotion_date": "2025-11-07"
}
```

**Response (400 Bad Request):**
```json
{
  "text_content": [
    "Text content is required when content_type is \"text\""
  ]
}
```

#### 2. Missing YouTube URL for Video

**Request:**
```json
{
  "title": "Video Test",
  "content_type": "video",
  "description": "Test video devotion",
  "devotion_date": "2025-11-07"
}
```

**Response (400 Bad Request):**
```json
{
  "youtube_url": [
    "YouTube URL is required when content_type is \"video\""
  ]
}
```

#### 3. Duplicate Date

**Response (400 Bad Request):**
```json
{
  "non_field_errors": [
    "The fields devotion_date must make a unique set."
  ]
}
```

#### 4. Unauthorized Access

**Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 5. Permission Denied

**Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 6. Not Found

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

## Permissions Summary

| Action | Endpoint | Permission Required |
|--------|----------|---------------------|
| List devotions | `GET /api/devotions/` | None (Public) |
| Get today's devotion | `GET /api/devotions/today/` | None (Public) |
| Get single devotion | `GET /api/devotions/{id}/` | None (Public) |
| Create devotion | `POST /api/devotions/` | Admin (`is_staff=True`) |
| Update devotion | `PUT/PATCH /api/devotions/{id}/` | Admin (`is_staff=True`) |
| Delete devotion | `DELETE /api/devotions/{id}/` | Admin (`is_staff=True`) |

---

## Best Practices

### For Admins

1. **Plan Ahead**: Create devotions in advance to ensure daily content
2. **Consistent Timing**: Upload devotions at the same time each day
3. **Quality Content**: Ensure text is well-formatted and videos are appropriate
4. **Unique Dates**: Only one devotion per date - plan your content calendar
5. **Test URLs**: Verify YouTube URLs work before publishing
6. **Mobile-Friendly**: Keep text concise and readable on mobile devices

### For Developers

1. **Cache Today's Devotion**: Consider caching the `/devotions/today/` response
2. **Handle Missing Devotions**: Show a friendly message if no devotion exists
3. **Preload Thumbnails**: Use the `thumbnail_url` for video previews
4. **Date Formatting**: Display dates in user's local format
5. **Offline Support**: Cache recent devotions for offline viewing
6. **Push Notifications**: Notify users when new devotions are available

### Content Guidelines

#### Text Devotions
- **Length**: 300-800 words ideal
- **Structure**: Introduction, main points, prayer/reflection
- **Formatting**: Use line breaks for readability
- **Scripture**: Include relevant Bible verses
- **Application**: Provide practical takeaways

#### Video Devotions
- **Duration**: 5-15 minutes recommended
- **Quality**: HD video preferred
- **Audio**: Clear audio is essential
- **Subtitles**: Enable YouTube captions
- **Description**: Provide context in the description field

---

## Data Structure

### Text Devotion Example
```json
{
  "id": 1,
  "title": "Finding Peace in Chaos",
  "content_type": "text",
  "description": "Discovering God's peace in difficult circumstances",
  "text_content": "In Philippians 4:7, we read about 'the peace of God, which transcends all understanding...'\n\nKey Points:\n1. God's peace is available to all believers\n2. It surpasses human understanding\n3. It guards our hearts and minds\n\nReflection Questions:\n- Where do you need God's peace today?\n- How can you cultivate peace in your daily life?\n\nPrayer: Father, grant me Your peace that surpasses understanding. Amen.",
  "youtube_url": null,
  "devotion_date": "2025-11-07",
  "created_at": "2025-11-06T08:00:00Z",
  "thumbnail_url": null
}
```

### Video Devotion Example
```json
{
  "id": 2,
  "title": "The Good Shepherd",
  "content_type": "video",
  "description": "Exploring Psalm 23 and Jesus as our shepherd",
  "text_content": null,
  "youtube_url": "https://www.youtube.com/watch?v=example456",
  "devotion_date": "2025-11-08",
  "created_at": "2025-11-07T08:00:00Z",
  "thumbnail_url": "https://img.youtube.com/vi/example456/maxresdefault.jpg"
}
```

---

## Migration Required

After implementing this API, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the `Devotion` table in your database.

---

## Quick Reference

### Supported YouTube URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

### Thumbnail Sizes Available
- `maxresdefault.jpg` - Maximum resolution (1920x1080)
- `sddefault.jpg` - Standard definition (640x480)
- `hqdefault.jpg` - High quality (480x360)
- `mqdefault.jpg` - Medium quality (320x180)
- `default.jpg` - Default thumbnail (120x90)

The API automatically uses `maxresdefault.jpg` for best quality.

---

## Support

For issues or questions about the Devotions API, contact your development team or refer to the main API documentation.
