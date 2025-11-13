# Live Streaming Functionality

This document outlines the live streaming functionality for the Ark of God application, allowing admins to manage live streams from multiple platforms including YouTube, Facebook, Vimeo, and Twitch.

## Features

- Support for multiple streaming platforms (YouTube, Facebook, Vimeo, Twitch)
- Schedule future streams with automatic activation
- Admin controls to manage live streams
- Only one active stream at a time
- Public endpoints to get active and upcoming streams
- Stream preview in admin interface

## Supported Platforms

- YouTube (youtube.com, youtu.be)
- Facebook (facebook.com, fb.watch)
- Vimeo (vimeo.com)
- Twitch (twitch.tv)

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
    "stream_url": "https://youtube.com/live/...",
    "is_live": true,
    "thumbnail_url": "https://.../thumbnail.jpg",
    "scheduled_time": "2023-11-15T10:00:00Z",
    "created_at": "2023-11-10T08:00:00Z",
    "updated_at": "2023-11-10T08:00:00Z"
}
```

### Get Upcoming Streams
```
GET /streams/upcoming/
```

**Response**
```json
[
    {
        "id": 2,
        "title": "Bible Study",
        "description": "Midweek Bible study session",
        "stream_url": "https://facebook.com/...",
        "is_live": false,
        "thumbnail_url": "https://.../bible-study.jpg",
        "scheduled_time": "2023-11-17T19:00:00Z",
        "created_at": "2023-11-10T08:30:00Z",
        "updated_at": "2023-11-10T08:30:00Z"
    }
]
```

### List All Streams (Admin Only)
```
GET /streams/
```

### Create a New Stream (Admin Only)
```
POST /streams/
```

**Request Body**
```json
{
    "title": "Sunday Service",
    "description": "Weekly Sunday service",
    "stream_url": "https://youtube.com/live/...",
    "thumbnail_url": "https://.../thumbnail.jpg",
    "scheduled_time": "2023-11-15T10:00:00Z"
}
```

### Go Live (Admin Only)
```
POST /streams/{id}/go-live/
```

### End Stream (Admin Only)
```
POST /streams/{id}/end-stream/
```

## Admin Interface

Admins can manage streams through the Django admin interface at `/admin`:

1. Navigate to the Streams section
2. Click "Add Stream"
3. Fill in the details:
   - Title: Name of the stream
   - Description: Optional description
   - Stream URL: URL of the live stream (supports multiple platforms)
   - Thumbnail URL: Optional preview image for the stream
   - Is Live: Check to make this the active stream
   - Scheduled Time: When this stream is scheduled to start (optional)
4. Click "Save"

### Admin Actions

- **Go Live**: Mark a stream as live (will automatically end any other live stream)
- **End Stream**: End the currently active stream
- **Remove Old Streams**: Clean up old, inactive streams

## Implementation Notes

- Only one stream can be active at a time
- When a new stream is marked as live, any currently active stream will be automatically stopped
- Streams can be scheduled for future dates
- The admin interface includes a preview of the stream
- Streams can be filtered by status in the admin interface
- Supports multiple streaming platforms with automatic URL validation

## Frontend Integration

To display the active stream in your frontend application:

1. Poll `/streams/active/` to check for active streams
2. If a stream is active, use the appropriate player based on the platform:

```javascript
// Example implementation
async function checkActiveStream() {
    try {
        const response = await fetch('/streams/active/');
        if (response.ok) {
            const stream = await response.json();
            if (stream) {
                displayStream(stream);
            } else {
                // No active stream
                checkUpcomingStreams();
            }
        }
    } catch (error) {
        console.error('Error checking active stream:', error);
    }
}

function displayStream(stream) {
    const container = document.getElementById('stream-container');
    
    if (stream.stream_url.includes('youtube.com') || stream.stream_url.includes('youtu.be')) {
        // YouTube embed
        const videoId = getYouTubeId(stream.stream_url);
        container.innerHTML = `
            <div class="video-container">
                <iframe 
                    width="100%" 
                    height="500" 
                    src="https://www.youtube.com/embed/${videoId}?autoplay=1" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
                <h2>${stream.title}</h2>
                <p>${stream.description || ''}</p>
            </div>
        `;
    } else if (stream.stream_url.includes('facebook.com') || stream.stream_url.includes('fb.watch')) {
        // Facebook embed
        container.innerHTML = `
            <div class="video-container">
                <div class="fb-video" 
                    data-href="${stream.stream_url}" 
                    data-width="100%" 
                    data-show-text="false">
                </div>
                <h2>${stream.title}</h2>
                <p>${stream.description || ''}</p>
            </div>
            <div id="fb-root"></div>
            <script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v12.0" 
                nonce="YOUR_NONCE"></script>
        `;
    } else if (stream.stream_url.includes('vimeo.com')) {
        // Vimeo embed
        const videoId = stream.stream_url.split('vimeo.com/')[1].split('?')[0];
        container.innerHTML = `
            <div class="video-container">
                <iframe 
                    src="https://player.vimeo.com/video/${videoId}" 
                    width="100%" 
                    height="500" 
                    frameborder="0" 
                    allow="autoplay; fullscreen; picture-in-picture" 
                    allowfullscreen>
                </iframe>
                <h2>${stream.title}</h2>
                <p>${stream.description || ''}</p>
            </div>
        `;
    } else if (stream.stream_url.includes('twitch.tv')) {
        // Twitch embed
        container.innerHTML = `
            <div class="video-container">
                <div id="twitch-embed"></div>
                <script src="https://embed.twitch.tv/embed/v1.js"></script>
                <script type="text/javascript">
                    new Twitch.Embed("twitch-embed", {
                        width: "100%",
                        height: 500,
                        channel: "${stream.stream_url.split('twitch.tv/')[1].split('/')[0]}",
                        layout: "video",
                        autoplay: true
                    });
                </script>
                <h2>${stream.title}</h2>
                <p>${stream.description || ''}</p>
            </div>
        `;
    }
}

// Check for new streams every 30 seconds
setInterval(checkActiveStream, 30000);
```
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
