# YouTube Streaming Functionality

This document outlines the YouTube streaming functionality for the Ark of God application, allowing admins to manage both live and pre-recorded YouTube content.

## Features

- Stream YouTube Live videos or regular YouTube videos
- Admin controls to start/stop streams
- Only one active stream at a time
- Public endpoint to get the currently active stream
- Simple YouTube URL-based setup

## API Endpoints

### Get Active Stream
```
GET /streams/active/
```

**Response**
```json
{
    "id": 1,
    "title": "Sunday Service",
    "description": "Weekly Sunday service",
    "stream_type": "youtube",
    "youtube_url": "https://youtube.com/...",
    "is_active": true,
    "start_time": "2023-11-08T10:00:00Z"
}
```

### List All Streams
```
GET /streams/
```

### Create a New Stream
```
POST /streams/
```

**Request Body**
```json
{
    "title": "Sunday Service",
    "description": "Weekly Sunday service",
    "stream_type": "live",
    "youtube_url": "https://youtube.com/..."
}
```

**Stream Types:**
- `live`: For YouTube Live streams
- `regular`: For pre-recorded YouTube videos

### Start a Stream (Admin Only)
```
POST /streams/{id}/start/
```

### End a Stream (Admin Only)
```
POST /streams/{id}/end/
```

## Admin Interface

Admins can manage streams through the Django admin interface at `/admin`:

1. Navigate to the Streams section
2. Click "Add Stream"
3. Fill in the details:
   - Title: Name of the stream
   - Description: Optional description
   - Stream Type: Choose between "YouTube Live" or "YouTube Video"
   - YouTube URL: Full URL of the YouTube video or live stream
4. Click "Save and continue editing"
5. Use the "Start" button to begin streaming
6. Use the "End" button to stop streaming

## Implementation Notes

- Only one stream can be active at a time
- When a new stream is started, any currently active stream will be automatically stopped
- The `is_active` field is managed automatically by the system
- Streams can be filtered by status and type in the admin interface
- Only YouTube URLs are supported (both live and regular videos)

## Frontend Integration

To display the active stream in your frontend application:

1. Poll `/streams/active/` to check for active streams
2. If a stream is active, use the YouTube iframe player with the provided URL:
   ```javascript
   // Example using YouTube IFrame Player API
   const player = new YT.Player('player', {
       height: '360',
       width: '640',
       videoId: 'EXTRACTED_FROM_YOUTUBE_URL',
       playerVars: {
           'autoplay': 1,
           'controls': 1,
           'rel': 0
       }
   });
   ```
3. Update the UI when the stream starts/stops

## Security

- Only authenticated admin users can create, update, or delete streams
- The active stream endpoint is public
- Only YouTube URLs are accepted (no file uploads)
- YouTube's own security measures apply to the embedded content
