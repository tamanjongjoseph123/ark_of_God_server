# Prayer Room Functionality

This document outlines the prayer room feature that allows admins to manage a single live prayer session with YouTube streaming and dynamic prayer topics.

## Features

- Single prayer room instance (singleton pattern)
- YouTube live or regular video streaming support
- Real-time prayer topic updates
- Public access to prayer room status
- Admin controls for starting/ending prayer sessions
- Secure admin-only endpoints for management

## API Endpoints

### Get Prayer Room Status
```
GET /api/prayer-room/
```
**Response**
```json
{
    "id": 1,
    "title": "Prayer Room",
    "description": "Join us for prayer",
    "is_active": true,
    "current_topic": "Healing and Restoration",
    "youtube_url": "https://youtube.com/...",
    "started_at": "2023-11-07T20:00:00Z",
    "created_at": "2023-11-07T19:30:00Z",
    "updated_at": "2023-11-07T20:05:00Z"
}
```

### Start Prayer Room (Admin Only)
```
POST /api/prayer-room/start/
```
**Request Body**
```json
{
    "youtube_url": "https://youtube.com/...",
    "title": "Evening Prayer",
    "description": "Join us for evening prayers",
    "current_topic": "Healing and Restoration"
}
```
**Response**
```json
{
    "status": "Prayer room started",
    "is_active": true,
    "youtube_url": "https://youtube.com/...",
    "started_at": "2023-11-07T20:00:00Z",
    "current_topic": "Healing and Restoration"
}
```

### End Prayer Room (Admin Only)
```
POST /api/prayer-room/end/
```
**Response**
```json
{
    "status": "Prayer room ended",
    "is_active": false,
    "ended_at": "2023-11-07T21:00:00Z"
}
```

### Update Prayer Topic (Admin Only)
```
POST /api/prayer-room/update_topic/
```
**Request Body**
```json
{
    "topic": "New prayer topic"
}
```
**Response**
```json
{
    "status": "Prayer topic updated",
    "current_topic": "New prayer topic"
}
```

## Admin Interface

1. **Prayer Room Management**:
   - Navigate to the Django admin panel
   - Click on "Prayer Room"
   - Update the prayer room details:
     - Title and description
     - Current prayer topic
     - YouTube URL (required for starting)
   - Save changes

2. **Start Prayer Session**:
   - Ensure a valid YouTube URL is set
   - Use the "Start prayer room" action
   - Or use the API: `POST /api/prayer-room/start/`

3. **End Prayer Session**:
   - Use the "End prayer room" action
   - Or use the API: `POST /api/prayer-room/end/`

4. **Update Prayer Topic**:
   - Edit the "Current topic" field in admin
   - Or use the API: `POST /api/prayer-room/update_topic/` with `{"topic": "New topic"}`

## Frontend Integration

### Displaying the Prayer Room

```javascript
// Fetch the prayer room status
const fetchPrayerRoom = async () => {
  try {
    const response = await fetch('/api/prayer-room/');
    const prayerRoom = await response.json();
    
    if (prayerRoom.is_active) {
      displayPrayerRoom(prayerRoom);
    } else {
      showPrayerRoomInactive();
    }
  } catch (error) {
    console.error('Error fetching prayer room:', error);
  }
};

// Display prayer room with YouTube player
const displayPrayerRoom = (prayerRoom) => {
  const container = document.getElementById('prayer-room-container');
  
  container.innerHTML = `
    <h2>${prayerRoom.title}</h2>
    ${prayerRoom.description ? `<p>${prayerRoom.description}</p>` : ''}
    
    ${prayerRoom.youtube_url ? `
      <div id="player"></div>
      <script src="https://www.youtube.com/iframe_api"></script>
      <script>
        function onYouTubeIframeAPIReady() {
          new YT.Player('player', {
            height: '360',
            width: '640',
            videoId: '${extractYouTubeId(prayerRoom.youtube_url)}',
            playerVars: {
              'autoplay': 1,
              'controls': 1,
              'rel': 0
            }
          });
        }
      </script>
    ` : ''}
    
    <div class="prayer-topic">
      <h3>Current Prayer Topic</h3>
      <p>${prayerRoom.current_topic || 'No topic set'}</p>
    </div>
  `;
};

// Helper function to extract YouTube video ID
const extractYouTubeId = (url) => {
  if (!url) return null;
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

// Poll for updates every 30 seconds
setInterval(fetchPrayerRoom, 30000);

// Initial load
fetchPrayerRoom();
```

## Security

- Admin endpoints require authentication and staff status
- The prayer room status endpoint is publicly accessible
- YouTube's security measures apply to embedded content

## Setup

1. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create a superuser (if needed):
   ```bash
   python manage.py createsuperuser
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

You can test the API using curl or any HTTP client:

```bash
# Get prayer room status (public)
curl http://localhost:8000/api/prayer-room/

# Start prayer room (admin only)
curl -X POST http://localhost:8000/api/prayer-room/start/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"youtube_url": "https://youtube.com/...", "title": "Prayer Session", "description": "Join us for prayer", "current_topic": "Healing"}'

# Update prayer topic (admin only)
curl -X POST http://localhost:8000/api/prayer-room/update_topic/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"topic": "New Prayer Topic"}'

# End prayer room (admin only)
curl -X POST http://localhost:8000/api/prayer-room/end/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update prayer topic (admin only)
curl -X POST http://localhost:8000/api/prayer-room/update_topic/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"topic": "New prayer topic"}'

# End prayer room (admin only)
curl -X POST http://localhost:8000/api/prayer-room/end/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```
