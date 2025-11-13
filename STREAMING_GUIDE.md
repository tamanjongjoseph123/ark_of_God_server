# How to Use the Live Stream Feature

## For Administrators

### Updating the Stream
1. **Log in** to the admin panel at `/admin`
2. Click on **Stream** in the sidebar
3. Update the stream details:
   - **Title**: Name of your stream (e.g., "Sunday Service")
   - **Description**: Optional details about the stream
   - **Stream URL**: The full URL of your live stream (YouTube, Facebook, etc.)
   - **Thumbnail URL**: Optional preview image (recommended: 1280x720px)
   - **Scheduled Time**: When the stream will start (optional)
4. Click **Save**

### Supported Platforms
- YouTube (live and regular videos)
- Facebook Live
- Vimeo
- Twitch
- Any platform with an embeddable iframe

### Best Practices
1. **Before Going Live**
   - Test your stream URL in the admin preview
   - Add a descriptive title and thumbnail
   - Set the scheduled time if applicable

2. **During Live Stream**
   - The stream will automatically appear on the website
   - No need to mark it as "live" - the system handles this

3. **After Streaming**
   - You can update the stream with a recording URL
   - Or clear the stream URL if no longer needed

## For Website Visitors

### Watching the Stream
1. Visit the website's stream page
2. The current stream will load automatically
3. If no stream is active, a message will be shown

### Troubleshooting
- **Stream not loading?**
  - Check if the URL is correct in the admin panel
  - Ensure the stream is actually live (if using a live platform)
  - Try refreshing the page

- **Video quality issues?**
  - Check your internet connection
  - The stream quality depends on the source platform's settings

## For Developers

### API Endpoints
- `GET /api/stream/current/` - Get current stream info (public)
- `PUT /api/stream/1/` - Update stream (admin only)

### Example API Response
```json
{
    "id": 1,
    "title": "Sunday Service",
    "description": "Join us for worship",
    "stream_url": "https://youtube.com/live/...",
    "thumbnail_url": "https://.../preview.jpg",
    "scheduled_time": "2023-11-15T10:00:00Z",
    "created_at": "2023-11-10T08:00:00Z",
    "updated_at": "2023-11-10T08:00:00Z"
}
```

### Embedding the Stream
Add this HTML to your page:
```html
<div id="stream-container">
    <!-- Stream will load here -->
</div>

<script>
// Fetch and display the stream
async function loadStream() {
    try {
        const response = await fetch('/api/stream/current/');
        const stream = await response.json();
        
        const container = document.getElementById('stream-container');
        if (stream.stream_url) {
            container.innerHTML = `
                <h2>${stream.title || 'Live Stream'}</h2>
                ${stream.description ? `<p>${stream.description}</p>` : ''}
                <div class="video-container">
                    <iframe 
                        src="${getEmbedUrl(stream.stream_url)}" 
                        frameborder="0" 
                        allowfullscreen
                        style="width: 100%; height: 500px;">
                    </iframe>
                </div>
            `;
        } else {
            container.innerHTML = '<p>No stream is currently available.</p>';
        }
    } catch (error) {
        console.error('Error loading stream:', error);
    }
}

// Helper function to convert URLs to embed format
function getEmbedUrl(url) {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
        const videoId = url.includes('youtube.com') 
            ? url.split('v=')[1]?.split('&')[0]
            : url.split('youtu.be/')[1]?.split('?')[0];
        return `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    }
    // Add other platforms as needed
    return url;
}

// Load the stream when the page loads
window.addEventListener('load', loadStream);
</script>
```

## Need Help?
Contact support at [your-email@example.com] for assistance with the streaming feature.
