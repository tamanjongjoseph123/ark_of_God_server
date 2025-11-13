# Events API - Complete Documentation

## Overview

The Events API allows admins to manage church events, categorized as either **upcoming** or **past** events. Users can view all events, filter by status, and search by location.

## Features

- **Event Status**: Categorize events as `upcoming` or `past`
- **Location Support**: Add event locations for easy filtering
- **Image Upload**: Attach event images/posters
- **Date Management**: Schedule events with specific dates and times
- **Admin Control**: Only staff users can create/edit events
- **Public Access**: All users can view events without authentication
- **Filtering**: Filter by status, location, or date

---

## Table of Contents

1. [Authentication](#authentication)
2. [Event Model](#event-model)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)

---

## Authentication

### Admin Access Required

Only authenticated admin users (with `is_staff=True`) can create, update, or delete events.

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

## Event Model

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Auto | Unique identifier |
| `title` | String | Yes | Event title/name |
| `description` | Text | Yes | Detailed event description |
| `image` | ImageField | No | Event poster/image |
| `youtube_url` | URL | No | YouTube URL for past event recording (only used when event_status is "past") |
| `event_date` | DateTime | Yes | Date and time of the event |
| `event_status` | String | Yes | Either `upcoming` or `past` (default: `upcoming`) |
| `location` | String | Optional | Event location/venue |
| `created_at` | DateTime | Auto | Timestamp of creation |

### Event Status Options

- **`upcoming`**: Events that haven't occurred yet or are currently happening
- **`past`**: Events that have already concluded. For past events, you can provide a YouTube URL to the recorded video.

---

## API Endpoints

### 1. List All Events

- **URL**: `/api/upcoming-events/`
- **Method**: `GET`
- **Permission**: AllowAny
- **Query Parameters**:
  - `event_status` (optional): Filter by `upcoming` or `past`
  - `location` (optional): Filter by location (case-insensitive partial match)

**Examples:**

```bash
# Get all events
curl http://localhost:8000/api/upcoming-events/

# Get only upcoming events
curl http://localhost:8000/api/upcoming-events/?event_status=upcoming

# Get only past events
curl http://localhost:8000/api/upcoming-events/?event_status=past

# Filter by location
curl http://localhost:8000/api/upcoming-events/?location=New%20York
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sunday Worship Service",
    "description": "Join us for our weekly worship service with praise, worship, and powerful preaching.",
    "image": "https://example.com/media/events/worship.jpg",
    "event_date": "2025-11-10T10:00:00Z",
    "event_status": "upcoming",
    "location": "Main Sanctuary, New York",
    "created_at": "2025-11-01T08:00:00Z"
  },
  {
    "id": 2,
    "title": "Youth Conference 2024",
    "description": "Annual youth conference with workshops, activities, and special speakers.",
    "image": "https://example.com/media/events/youth-conf.jpg",
    "event_date": "2025-10-15T09:00:00Z",
    "event_status": "past",
    "location": "Convention Center, Los Angeles",
    "created_at": "2025-09-01T10:00:00Z"
  }
]
```

### 2. Get Upcoming Events Only (Special Endpoint)

- **URL**: `/api/upcoming-events/upcoming/`
- **Method**: `GET`
- **Permission**: AllowAny

**Example:**
```bash
curl http://localhost:8000/api/upcoming-events/upcoming/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sunday Worship Service",
    "description": "Join us for our weekly worship service",
    "image": "https://example.com/media/events/worship.jpg",
    "event_date": "2025-11-10T10:00:00Z",
    "event_status": "upcoming",
    "location": "Main Sanctuary",
    "created_at": "2025-11-01T08:00:00Z"
  }
]
```

### 3. Get Past Events Only (Special Endpoint)

- **URL**: `/api/upcoming-events/past/`
- **Method**: `GET`
- **Permission**: AllowAny

**Example:**
```bash
curl http://localhost:8000/api/upcoming-events/past/
```

**Response:**
```json
[
  {
    "id": 2,
    "title": "Youth Conference 2024",
    "description": "Annual youth conference",
    "image": "https://example.com/media/events/youth-conf.jpg",
    "event_date": "2025-10-15T09:00:00Z",
    "event_status": "past",
    "location": "Convention Center",
    "created_at": "2025-09-01T10:00:00Z"
  }
]
```

### 4. Get Single Event

- **URL**: `/api/upcoming-events/{id}/`
- **Method**: `GET`
- **Permission**: AllowAny

**Example:**
```bash
curl http://localhost:8000/api/upcoming-events/1/
```

### 5. Create an Event

- **URL**: `/api/upcoming-events/`
- **Method**: `POST`
- **Permission**: IsAdminUser (requires authentication)
- **Content-Type**: `multipart/form-data`

**Fields:**
- `title` (required): string
- `description` (required): string
- `image` (required): file upload
- `event_date` (required): datetime (ISO 8601 format)
- `event_status` (optional): `upcoming` or `past` (default: `upcoming`)
- `location` (optional): string

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Christmas Celebration" \
  -F description="Join us for a special Christmas service with carols, drama, and fellowship." \
  -F event_date="2025-12-25T18:00:00Z" \
  -F event_status="upcoming" \
  -F location="Main Church Building" \
  -F image=@/path/to/christmas-poster.jpg
```

**Response:**
```json
{
  "id": 3,
  "title": "Christmas Celebration",
  "description": "Join us for a special Christmas service with carols, drama, and fellowship.",
  "image": "https://example.com/media/events/christmas-poster.jpg",
  "event_date": "2025-12-25T18:00:00Z",
  "event_status": "upcoming",
  "location": "Main Church Building",
  "created_at": "2025-11-07T10:00:00Z"
}
```

### 6. Update an Event

- **URL**: `/api/upcoming-events/{id}/`
- **Methods**: `PUT` (full update), `PATCH` (partial update)
- **Permission**: IsAdminUser

**PATCH Example (partial update):**
```bash
curl -X PATCH http://localhost:8000/api/upcoming-events/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Sunday Worship Service - Updated" \
  -F location="New Sanctuary Building"
```

**PUT Example (full update):**
```bash
curl -X PUT http://localhost:8000/api/upcoming-events/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Sunday Worship Service" \
  -F description="Updated description" \
  -F event_date="2025-11-10T10:00:00Z" \
  -F event_status="upcoming" \
  -F location="Main Sanctuary" \
  -F image=@/path/to/new-image.jpg
```

### 7. Mark Event as Past

- **URL**: `/api/upcoming-events/{id}/`
- **Method**: `PATCH`
- **Permission**: IsAdminUser

**Example:**
```bash
curl -X PATCH http://localhost:8000/api/upcoming-events/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_status="past"
```

### 8. Delete an Event

- **URL**: `/api/upcoming-events/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/upcoming-events/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
*Status: 204 No Content*

---

## Usage Examples

### Scenario 1: Admin Creates Multiple Events

```bash
# Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

export TOKEN="your_token_here"

# Create upcoming event
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Prayer Night" \
  -F description="Join us for a night of powerful prayer and intercession" \
  -F event_date="2025-11-15T19:00:00Z" \
  -F event_status="upcoming" \
  -F location="Prayer Hall, Main Building" \
  -F image=@prayer-night.jpg

# Create another upcoming event
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Bible Study" \
  -F description="Weekly Bible study on the book of Romans" \
  -F event_date="2025-11-12T18:30:00Z" \
  -F event_status="upcoming" \
  -F location="Fellowship Hall" \
  -F image=@bible-study.jpg

# Add a past event for records
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Easter Service 2024" \
  -F description="Resurrection Sunday celebration" \
  -F event_date="2024-03-31T09:00:00Z" \
  -F event_status="past" \
  -F location="Main Sanctuary" \
  -F image=@easter-2024.jpg
```

### Scenario 2: User Browses Events on Mobile App

```bash
# View all upcoming events (no auth required)
curl http://localhost:8000/api/upcoming-events/upcoming/

# View all past events
curl http://localhost:8000/api/upcoming-events/past/

# Search events by location
curl http://localhost:8000/api/upcoming-events/?location=Main%20Sanctuary

# Get details of specific event
curl http://localhost:8000/api/upcoming-events/5/
```

### Scenario 3: Admin Updates Event After It Occurs

```bash
# Event has passed, mark it as past
curl -X PATCH http://localhost:8000/api/upcoming-events/3/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_status="past"

# Update event with additional details
curl -X PATCH http://localhost:8000/api/upcoming-events/3/ \
  -H "Authorization: Bearer $TOKEN" \
  -F description="Christmas Celebration - Over 500 attendees! Amazing night of worship and fellowship."
```

### Scenario 4: Admin Manages Event Lifecycle

```bash
# Create event
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Missions Conference" \
  -F description="Annual missions conference" \
  -F event_date="2025-11-20T09:00:00Z" \
  -F event_status="upcoming" \
  -F location="Conference Center" \
  -F image=@missions-conf.jpg

# Update event details before it happens
curl -X PATCH http://localhost:8000/api/upcoming-events/10/ \
  -H "Authorization: Bearer $TOKEN" \
  -F location="Updated: Grand Conference Hall"

# After event, mark as past
curl -X PATCH http://localhost:8000/api/upcoming-events/10/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_status="past"
```

---

## Error Handling

### Common Errors

#### 1. Missing Required Fields

**Request:**
```bash
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Test Event"
```

**Response (400 Bad Request):**
```json
{
  "description": ["This field is required."],
  "image": ["No file was submitted."],
  "event_date": ["This field is required."]
}
```

#### 2. Invalid Date Format

**Request:**
```bash
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F title="Test" \
  -F description="Test" \
  -F event_date="invalid-date" \
  -F image=@test.jpg
```

**Response (400 Bad Request):**
```json
{
  "event_date": [
    "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
  ]
}
```

#### 3. Invalid Event Status

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/upcoming-events/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_status="invalid"
```

**Response (400 Bad Request):**
```json
{
  "event_status": [
    "\"invalid\" is not a valid choice."
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

#### 6. Event Not Found

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
| List all events | `GET /api/upcoming-events/` | None (Public) |
| Get upcoming events | `GET /api/upcoming-events/upcoming/` | None (Public) |
| Get past events | `GET /api/upcoming-events/past/` | None (Public) |
| Get single event | `GET /api/upcoming-events/{id}/` | None (Public) |
| Create event | `POST /api/upcoming-events/` | Admin (`is_staff=True`) |
| Update event | `PUT/PATCH /api/upcoming-events/{id}/` | Admin (`is_staff=True`) |
| Delete event | `DELETE /api/upcoming-events/{id}/` | Admin (`is_staff=True`) |

---

## Best Practices

### For Admins

1. **Event Status Management**
   - Create events with `event_status=upcoming`
   - After the event concludes, update to `event_status=past`
   - Keep past events for historical records

2. **Image Guidelines**
   - Use high-quality images (minimum 800x600px)
   - Keep file sizes reasonable (under 5MB)
   - Use descriptive filenames
   - Ensure images are properly formatted (JPG, PNG)

3. **Date & Time**
   - Use ISO 8601 format: `YYYY-MM-DDThh:mm:ssZ`
   - Include timezone information
   - Double-check dates before publishing

4. **Location Details**
   - Be specific (e.g., "Main Sanctuary, 123 Church St")
   - Include building/room names
   - Add parking or access instructions in description

5. **Descriptions**
   - Write clear, engaging descriptions
   - Include key details (time, dress code, registration info)
   - Mention special guests or activities
   - Add contact information if needed

### For Developers

1. **Filtering**
   - Use `?event_status=upcoming` for event listings
   - Implement location-based search with the location parameter
   - Cache frequently accessed event lists

2. **Date Handling**
   - Convert dates to user's local timezone
   - Show countdown timers for upcoming events
   - Display "Past Event" badges for concluded events

3. **Image Display**
   - Implement lazy loading for event images
   - Provide fallback images for missing posters
   - Optimize images for mobile devices

4. **User Experience**
   - Show upcoming events prominently
   - Allow users to filter by location
   - Implement calendar view for events
   - Add "Add to Calendar" functionality

---

## Event Lifecycle

### Typical Event Flow

```
1. Admin creates event with event_status="upcoming"
   ↓
2. Event appears in upcoming events list
   ↓
3. Users view and register for the event
   ↓
4. Event date arrives and event takes place
   ↓
5. Admin updates event_status to "past"
   ↓
6. Event moves to past events archive
   ↓
7. Event remains accessible for historical reference
```

---

## Date Format Examples

### Valid Date Formats

```
2025-11-15T10:00:00Z          # UTC time
2025-11-15T10:00:00+00:00     # UTC with explicit offset
2025-11-15T10:00:00-05:00     # EST (UTC-5)
2025-11-15T10:00:00.123456Z   # With microseconds
```

### Creating Events with Different Timezones

```bash
# Event in UTC
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_date="2025-11-15T10:00:00Z" \
  ...

# Event in EST (UTC-5)
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_date="2025-11-15T10:00:00-05:00" \
  ...

# Event in PST (UTC-8)
curl -X POST http://localhost:8000/api/upcoming-events/ \
  -H "Authorization: Bearer $TOKEN" \
  -F event_date="2025-11-15T10:00:00-08:00" \
  ...
```

---

## Integration Examples

### React/React Native Example

```javascript
// Fetch upcoming events
const fetchUpcomingEvents = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/upcoming-events/upcoming/');
    const events = await response.json();
    return events;
  } catch (error) {
    console.error('Error fetching events:', error);
  }
};

// Create new event (admin only)
const createEvent = async (eventData, token) => {
  const formData = new FormData();
  formData.append('title', eventData.title);
  formData.append('description', eventData.description);
  formData.append('event_date', eventData.event_date);
  formData.append('event_status', 'upcoming');
  formData.append('location', eventData.location);
  formData.append('image', eventData.image);

  try {
    const response = await fetch('http://localhost:8000/api/upcoming-events/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    const newEvent = await response.json();
    return newEvent;
  } catch (error) {
    console.error('Error creating event:', error);
  }
};

// Mark event as past
const markEventAsPast = async (eventId, token) => {
  const formData = new FormData();
  formData.append('event_status', 'past');

  try {
    const response = await fetch(`http://localhost:8000/api/upcoming-events/${eventId}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    const updatedEvent = await response.json();
    return updatedEvent;
  } catch (error) {
    console.error('Error updating event:', error);
  }
};
```

---

## Migration Required

After implementing these changes, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will add the `event_status` and `location` fields to the `UpcomingEvent` table.

---

## Quick Reference

### Event Status Values
- `upcoming` - Events that haven't occurred yet
- `past` - Events that have already concluded

### Special Endpoints
- `/api/upcoming-events/upcoming/` - Get only upcoming events
- `/api/upcoming-events/past/` - Get only past events

### Query Parameters
- `?event_status=upcoming` - Filter by status
- `?event_status=past` - Filter by status
- `?location=New York` - Filter by location (partial match)

---

## Support

For issues or questions about the Events API, contact your development team or refer to the main API documentation.
