# Video Translations API Documentation

## Overview

The Video Translations API allows administrators to add translations for videos and enables mobile app users to fetch videos with their available translations and switch between different language versions.

## Features

- **Flexible Language Support**: Admins can add translations for any language without being restricted to predefined choices
- **Dual Video Support**: Works with both general videos (`Video` model) and course videos (`CourseVideo` model)
- **Admin Management**: Full Django admin interface for managing translations
- **Mobile App Integration**: API endpoints for fetching videos with translations

## API Endpoints

### Base URL: `/api/video-translations/`

### 1. List All Translations
```
GET /api/video-translations/
```

**Query Parameters:**
- `video_type` (optional): Filter by video type (`video` or `coursevideo`)
- `video_id` (optional): Filter by specific video ID
- `language` (optional): Filter by specific language code

**Response:**
```json
[
    {
        "id": 1,
        "video_type": "video",
        "video_id": 5,
        "language": "fr",
        "language_display": "French",
        "translated_video_url": "https://youtube.com/watch?v=...",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }
]
```

### 2. Create Translation
```
POST /api/video-translations/
```

**Request Body:**
```json
{
    "video_type": "video",
    "video_id": 5,
    "language": "fr",
    "language_display": "French",
    "translated_video_url": "https://youtube.com/watch?v=..."
}
```

**Response:**
```json
{
    "id": 1,
    "video_type": "video",
    "video_id": 5,
    "language": "fr",
    "language_display": "French",
    "translated_video_url": "https://youtube.com/watch?v=...",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

### 3. Get Translations for Specific Video
```
GET /api/video-translations/by_video/?video_type=video&video_id=5
```

**Response:**
```json
[
    {
        "id": 1,
        "video_type": "video",
        "video_id": 5,
        "language": "fr",
        "language_display": "French",
        "translated_video_url": "https://youtube.com/watch?v=...",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    {
        "id": 2,
        "video_type": "video",
        "video_id": 5,
        "language": "es",
        "language_display": "Spanish",
        "translated_video_url": "https://youtube.com/watch?v=...",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }
]
```

### 4. Update Translation
```
PUT /api/video-translations/{id}/
```

**Request Body:**
```json
{
    "video_type": "video",
    "video_id": 5,
    "language": "fr",
    "language_display": "French",
    "translated_video_url": "https://youtube.com/watch?v=..."
}
```

### 5. Delete Translation
```
DELETE /api/video-translations/{id}/
```

## Enhanced Video Endpoints

### Videos with Translations
The existing video endpoints now include translations:

#### Get Videos with Translations
```
GET /api/videos/
```

**Response:**
```json
[
    {
        "id": 5,
        "title": "Powerful Prophecy",
        "youtube_url": "https://youtube.com/watch?v=...",
        "category": "prophecy",
        "created_at": "2024-01-01T10:00:00Z",
        "translations": [
            {
                "id": 1,
                "video_type": "video",
                "video_id": 5,
                "language": "fr",
                "language_display": "French",
                "translated_video_url": "https://youtube.com/watch?v=...",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "video_type": "video",
                "video_id": 5,
                "language": "es",
                "language_display": "Spanish",
                "translated_video_url": "https://youtube.com/watch?v=...",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        ]
    }
]
```

#### Get Course Videos with Translations
```
GET /api/course-videos/
```

**Response:**
```json
[
    {
        "id": 12,
        "name": "Chapter 1: Introduction",
        "description": "Introduction to the course",
        "youtube_url": "https://youtube.com/watch?v=...",
        "key_takeaways": "Key points from this lesson",
        "assignments": "Practice exercises",
        "created_at": "2024-01-01T10:00:00Z",
        "translations": [
            {
                "id": 3,
                "video_type": "coursevideo",
                "video_id": 12,
                "language": "fr",
                "language_display": "French",
                "translated_video_url": "https://youtube.com/watch?v=...",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        ]
    }
]
```

## Admin Interface

### Video Translation Admin

The Django admin interface provides:

1. **List View**: Shows all translations with video info, language, and URLs
2. **Search**: Search by language display name or translated video URL
3. **Filters**: Filter by video type, language, or creation date
4. **Fieldsets**: Organized into logical sections:
   - Video Information: Video type and ID
   - Translation Details: Language and translated URL
   - Timestamps: Creation and update dates

### Adding Translations

1. Navigate to **Video Translations** in Django admin
2. Click **Add Video Translation**
3. Fill in the form:
   - **Video Type**: Choose "General Video" or "Course Video"
   - **Video ID**: Enter the ID of the video
   - **Language**: Enter language code (e.g., "fr", "es")
   - **Language Display**: Enter display name (e.g., "French", "Spanish")
   - **Translated Video URL**: Enter the URL of the translated video

### Updating Existing Videos

For existing videos, admins can:
1. Go to the video (Video or CourseVideo) in admin
2. Add translations using the Video Translation interface
3. The system will automatically validate that the video exists

## Mobile App Integration

### Fetching Videos with Translations

When the mobile app fetches videos, it will receive both the original video URL and all available translations:

```javascript
// Example mobile app implementation
async function fetchVideoWithTranslations(videoId, videoType) {
    const response = await fetch(`/api/${videoType}s/${videoId}/`);
    const video = response.data;
    
    // Original video
    const originalVideo = {
        url: video.youtube_url,
        title: video.title,
        // ... other video properties
    };
    
    // Available translations
    const translations = video.translations.map(t => ({
        language: t.language,
        languageDisplay: t.language_display,
        url: t.translated_video_url
    }));
    
    return {
        originalVideo,
        translations
    };
}
```

### Language Switching

The mobile app can implement language switching:

```javascript
function switchToTranslation(video, translations, languageCode) {
    const translation = translations.find(t => t.language === languageCode);
    
    if (translation) {
        // Switch to the translated video
        return {
            url: translation.translated_video_url,
            language: translation.languageDisplay,
            isTranslated: true
        };
    } else {
        // Fall back to original if translation not found
        return {
            url: video.youtube_url,
            language: 'Original',
            isTranslated: false
        };
    }
}
```

## Usage Examples

### Example 1: Adding French Translation to a Video

1. **Admin Action:**
   - Go to Django admin → Video Translations → Add
   - Video Type: "General Video"
   - Video ID: 42
   - Language: "fr"
   - Language Display: "French"
   - Translated Video URL: "https://youtube.com/watch?v=french_version"

2. **Mobile App Result:**
   - User fetches the video
   - App shows both original and French translation options
   - User can tap "Français" to switch to French version

### Example 2: Adding Spanish Translation to a Course Video

1. **Admin Action:**
   - Go to Django admin → Video Translations → Add
   - Video Type: "Course Video"
   - Video ID: 15
   - Language: "es"
   - Language Display: "Spanish"
   - Translated Video URL: "https://youtube.com/watch?v=spanish_version"

2. **Mobile App Result:**
   - User watching course lesson sees original video
   - Language selector shows "Español" option
   - Tapping switches to Spanish version of the lesson

## Error Handling

### Common Errors

1. **Video Not Found** (400):
   ```json
   {
       "video_id": ["Video with ID 999 does not exist"]
   }
   ```

2. **Duplicate Translation** (400):
   ```json
   {
       "non_field_errors": {
           "video_type": ["Video translation with this video type and language already exists"]
       }
   }
   ```

## Best Practices

1. **Language Codes**: Use standard ISO 639-1 codes (en, fr, es, de, etc.)
2. **URL Validation**: Ensure all video URLs are valid and accessible
3. **Display Names**: Use user-friendly language display names
4. **Consistency**: Maintain consistent naming across translations
5. **Testing**: Test translations in mobile app before publishing

## Security

- Admin permissions required for creating/updating/deleting translations
- Public read access for mobile app users
- Video existence validation prevents orphaned translations
- URL validation ensures only valid video URLs are stored
