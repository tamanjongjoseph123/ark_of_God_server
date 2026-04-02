# Pagination API Documentation

## Overview

All paginated endpoints in the API use Django REST Framework's `PageNumberPagination` with the following configuration:

- **Default Page Size**: 10 items per page
- **Page Size Parameter**: `page_size`
- **Page Number Parameter**: `page`

## Response Format

Paginated responses follow this structure:

```json
{
    "count": 125,
    "next": "http://localhost:8000/api/videos/?page=3",
    "previous": "http://localhost:8000/api/videos/?page=1",
    "results": [
        {
            "id": 1,
            "title": "Video Title",
            "youtube_url": "https://youtube.com/watch?v=...",
            "category": "prophecy",
            "created_at": "2024-01-01T10:00:00Z"
        }
        // ... more items
    ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Total number of items across all pages |
| `next` | string\|null | URL to the next page (null if on last page) |
| `previous` | string\|null | URL to the previous page (null if on first page) |
| `results` | array | Array of items for the current page |

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number to retrieve |
| `page_size` | integer | 10 | Number of items per page (max: 100) |

## Endpoints with Pagination

### Videos API

#### Get All Videos (Paginated)
```
GET /api/videos/
```

**Example Requests:**

Get first page (default):
```
GET /api/videos/
```

Get specific page:
```
GET /api/videos/?page=2
```

Custom page size:
```
GET /api/videos/?page_size=20
```

Both page and page_size:
```
GET /api/videos/?page=2&page_size=5
```

**Response Example:**
```json
{
    "count": 45,
    "next": "http://localhost:8000/api/videos/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Prophetic Healing Service",
            "youtube_url": "https://youtube.com/watch?v=abc123",
            "category": "prophecy",
            "created_at": "2024-01-01T10:00:00Z"
        },
        {
            "id": 2,
            "title": "Crusade Highlights",
            "youtube_url": "https://youtube.com/watch?v=def456",
            "category": "crusades",
            "created_at": "2024-01-02T15:30:00Z"
        }
        // ... 8 more items
    ]
}
```

#### Get Videos by Category (Paginated)
```
GET /api/videos/by_category/?category={category}
```

**Example:**
```
GET /api/videos/by_category/?category=prophecy&page=1&page_size=10
```

### Course Videos API

#### Get All Course Videos (Paginated)
```
GET /api/course-videos/
```

#### Get Course Videos by Course (Paginated)
```
GET /api/course-videos/?course_id={course_id}
```

### Other Paginated Endpoints

The following endpoints also support pagination:

- `/api/church-projects/`
- `/api/inspiration-quotes/`
- `/api/prayer-requests/`
- `/api/testimonies/`
- `/api/upcoming-events/`
- `/api/devotions/`
- `/api/video-translations/`

### Prayer Requests API

#### Get All Prayer Requests (Paginated)
```
GET /api/prayer-requests/
```

**Example Requests:**

Get first page (default 10 items):
```
GET /api/prayer-requests/
```

Get specific page with custom page size:
```
GET /api/prayer-requests/?page=2&page_size=15
```

**Response Example:**
```json
{
    "count": 5078,
    "next": "http://localhost:8000/api/prayer-requests/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5081,
            "name": "John Doe",
            "email": "john@example.com",
            "phone_number": "+1234567890",
            "country": "United States",
            "request": "Please pray for my family's health and wellbeing. We are going through difficult times.",
            "created_at": "2024-01-15T14:30:00Z"
        },
        {
            "id": 5080,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone_number": "+0987654321",
            "country": "Canada",
            "request": "Pray for my job search and financial stability.",
            "created_at": "2024-01-15T12:15:00Z"
        }
        // ... 8 more items
    ]
}
```

#### Create New Prayer Request
```
POST /api/prayer-requests/
```

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "country": "United States",
    "request": "Please pray for my family's health and wellbeing."
}
```

**Response (201 Created):**
```json
{
    "id": 5082,
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "country": "United States",
    "request": "Please pray for my family's health and wellbeing.",
    "created_at": "2024-01-15T16:45:00Z"
}
```

## Client-Side Implementation

### JavaScript/Fetch Example

```javascript
async function fetchVideos(page = 1, pageSize = 10) {
    try {
        const response = await fetch(`/api/videos/?page=${page}&page_size=${pageSize}`);
        const data = await response.json();
        
        console.log('Total videos:', data.count);
        console.log('Current page videos:', data.results);
        console.log('Next page URL:', data.next);
        console.log('Previous page URL:', data.previous);
        
        return data;
    } catch (error) {
        console.error('Error fetching videos:', error);
    }
}

// Usage
fetchVideos(1, 10); // First page, 10 items
```

### JavaScript/Fetch Example for Prayer Requests

```javascript
async function fetchPrayerRequests(page = 1, pageSize = 10) {
    try {
        const response = await fetch(`/api/prayer-requests/?page=${page}&page_size=${pageSize}`);
        const data = await response.json();
        
        console.log('Total prayer requests:', data.count);
        console.log('Current page requests:', data.results);
        console.log('Next page URL:', data.next);
        console.log('Previous page URL:', data.previous);
        
        return data;
    } catch (error) {
        console.error('Error fetching prayer requests:', error);
    }
}

async function createPrayerRequest(prayerData) {
    try {
        const response = await fetch('/api/prayer-requests/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(prayerData)
        });
        
        if (response.ok) {
            const newRequest = await response.json();
            console.log('Prayer request created:', newRequest);
            return newRequest;
        } else {
            const error = await response.json();
            console.error('Error creating prayer request:', error);
            throw error;
        }
    } catch (error) {
        console.error('Error creating prayer request:', error);
        throw error;
    }
}

// Usage examples
fetchPrayerRequests(1, 10); // First page, 10 requests

// Create new prayer request
const newPrayer = {
    name: "John Doe",
    email: "john@example.com",
    phone_number: "+1234567890",
    country: "United States",
    request: "Please pray for my family's health and wellbeing."
};
createPrayerRequest(newPrayer);
```

### React Example

```jsx
import React, { useState, useEffect } from 'react';

function VideoList() {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [totalCount, setTotalCount] = useState(0);

    const fetchVideos = async (page = 1) => {
        setLoading(true);
        try {
            const response = await fetch(`/api/videos/?page=${page}&page_size=10`);
            const data = await response.json();
            
            setVideos(data.results);
            setTotalCount(data.count);
            setTotalPages(Math.ceil(data.count / 10));
            setCurrentPage(page);
        } catch (error) {
            console.error('Error fetching videos:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVideos(1);
    }, []);

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages) {
            fetchVideos(newPage);
        }
    };

    return (
        <div>
            <h2>Videos ({totalCount})</h2>
            
            {loading ? (
                <div>Loading...</div>
            ) : (
                <>
                    {videos.map(video => (
                        <div key={video.id}>
                            <h3>{video.title}</h3>
                            <p>Category: {video.category}</p>
                            <a href={video.youtube_url} target="_blank">Watch Video</a>
                        </div>
                    ))}
                    
                    <div className="pagination">
                        <button 
                            onClick={() => handlePageChange(currentPage - 1)}
                            disabled={currentPage === 1}
                        >
                            Previous
                        </button>
                        
                        <span>
                            Page {currentPage} of {totalPages}
                        </span>
                        
                        <button 
                            onClick={() => handlePageChange(currentPage + 1)}
                            disabled={currentPage === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
```

### React Example for Prayer Requests

```jsx
import React, { useState, useEffect } from 'react';

function PrayerRequestList() {
    const [prayerRequests, setPrayerRequests] = useState([]);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [totalCount, setTotalCount] = useState(0);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone_number: '',
        country: '',
        request: ''
    });

    const fetchPrayerRequests = async (page = 1) => {
        setLoading(true);
        try {
            const response = await fetch(`/api/prayer-requests/?page=${page}&page_size=10`);
            const data = await response.json();
            
            setPrayerRequests(data.results);
            setTotalCount(data.count);
            setTotalPages(Math.ceil(data.count / 10));
            setCurrentPage(page);
        } catch (error) {
            console.error('Error fetching prayer requests:', error);
        } finally {
            setLoading(false);
        }
    };

    const createPrayerRequest = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/prayer-requests/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                const newRequest = await response.json();
                setPrayerRequests([newRequest, ...prayerRequests]);
                setTotalCount(totalCount + 1);
                setFormData({
                    name: '',
                    email: '',
                    phone_number: '',
                    country: '',
                    request: ''
                });
                setShowForm(false);
                alert('Prayer request submitted successfully!');
            } else {
                alert('Error submitting prayer request. Please try again.');
            }
        } catch (error) {
            console.error('Error creating prayer request:', error);
            alert('Error submitting prayer request. Please try again.');
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages) {
            fetchPrayerRequests(newPage);
        }
    };

    useEffect(() => {
        fetchPrayerRequests(1);
    }, []);

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Prayer Requests ({totalCount})</h2>
                <button 
                    onClick={() => setShowForm(!showForm)}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    {showForm ? 'Cancel' : 'New Prayer Request'}
                </button>
            </div>

            {showForm && (
                <form onSubmit={createPrayerRequest} style={{
                    backgroundColor: '#f8f9fa',
                    padding: '20px',
                    borderRadius: '5px',
                    marginBottom: '20px'
                }}>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px' }}>Name:</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                            style={{ width: '100%', padding: '8px', borderRadius: '3px', border: '1px solid #ddd' }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            style={{ width: '100%', padding: '8px', borderRadius: '3px', border: '1px solid #ddd' }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px' }}>Phone Number:</label>
                        <input
                            type="tel"
                            name="phone_number"
                            value={formData.phone_number}
                            onChange={handleInputChange}
                            required
                            style={{ width: '100%', padding: '8px', borderRadius: '3px', border: '1px solid #ddd' }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px' }}>Country:</label>
                        <input
                            type="text"
                            name="country"
                            value={formData.country}
                            onChange={handleInputChange}
                            required
                            style={{ width: '100%', padding: '8px', borderRadius: '3px', border: '1px solid #ddd' }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px' }}>Prayer Request:</label>
                        <textarea
                            name="request"
                            value={formData.request}
                            onChange={handleInputChange}
                            required
                            rows="4"
                            style={{ width: '100%', padding: '8px', borderRadius: '3px', border: '1px solid #ddd' }}
                        />
                    </div>
                    
                    <button 
                        type="submit"
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#28a745',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                    >
                        Submit Prayer Request
                    </button>
                </form>
            )}
            
            {loading ? (
                <div>Loading prayer requests...</div>
            ) : (
                <>
                    {prayerRequests.map(request => (
                        <div key={request.id} style={{
                            backgroundColor: '#fff',
                            padding: '15px',
                            marginBottom: '10px',
                            borderRadius: '5px',
                            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                        }}>
                            <h4 style={{ margin: '0 0 10px 0', color: '#333' }}>{request.name}</h4>
                            <p style={{ margin: '5px 0', fontSize: '14px', color: '#666' }}>
                                <strong>Email:</strong> {request.email}
                            </p>
                            <p style={{ margin: '5px 0', fontSize: '14px', color: '#666' }}>
                                <strong>Phone:</strong> {request.phone_number}
                            </p>
                            <p style={{ margin: '5px 0', fontSize: '14px', color: '#666' }}>
                                <strong>Country:</strong> {request.country}
                            </p>
                            <p style={{ margin: '10px 0', lineHeight: '1.5' }}>{request.request}</p>
                            <small style={{ color: '#999' }}>
                                {new Date(request.created_at).toLocaleString()}
                            </small>
                        </div>
                    ))}
                    
                    {totalPages > 1 && (
                        <div className="pagination" style={{
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            gap: '10px',
                            marginTop: '20px'
                        }}>
                            <button 
                                onClick={() => handlePageChange(currentPage - 1)}
                                disabled={currentPage === 1}
                                style={{
                                    padding: '8px 16px',
                                    backgroundColor: currentPage === 1 ? '#ccc' : '#007bff',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '3px',
                                    cursor: currentPage === 1 ? 'not-allowed' : 'pointer'
                                }}
                            >
                                Previous
                            </button>
                            
                            <span>
                                Page {currentPage} of {totalPages}
                            </span>
                            
                            <button 
                                onClick={() => handlePageChange(currentPage + 1)}
                                disabled={currentPage === totalPages}
                                style={{
                                    padding: '8px 16px',
                                    backgroundColor: currentPage === totalPages ? '#ccc' : '#007bff',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '3px',
                                    cursor: currentPage === totalPages ? 'not-allowed' : 'pointer'
                                }}
                            >
                                Next
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
```
```

## Error Handling

### Common Error Responses

**Invalid Page Number:**
```json
{
    "detail": "Invalid page."
}
```

**Page Size Too Large:**
```json
{
    "page_size": [
        "Ensure this value is less than or equal to 100."
    ]
}
```

## Performance Considerations

1. **Default Page Size**: Set to 10 to balance between user experience and performance
2. **Maximum Page Size**: Limited to 100 to prevent excessive database queries
3. **Caching**: Consider implementing caching for frequently accessed pages
4. **Database Indexing**: Ensure proper indexes on fields used for filtering and ordering

## Admin Panel Integration

The Django admin panel automatically uses pagination for list views. The pagination settings will:

- Show 10 items per page by default in admin lists
- Allow admins to change page size using the admin interface
- Provide navigation controls for browsing through large datasets

To customize admin pagination for specific models:

```python
# in admin.py
from django.contrib import admin

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_per_page = 10  # Override default for this model
    list_max_show_all = 100  # Maximum items when "Show all" is clicked
```
