# API Pagination Documentation


```

## Pagination Parameters

All paginated endpoints support these query parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number to retrieve |
| `page_size` | integer | 10 | Number of items per page (max: 100) |

## Paginated Endpoints

### Videos
```
GET /api/videos/
```

**Query Parameters:**
- `page` (optional): Page number
- `page_size` (optional): Items per page
- `category` (optional): Filter by category (prophecy, crusades, testimonies, etc.)

**Example Requests:**
```bash
# First page, default 10 items
GET /api/videos/

# Page 2, 10 items
GET /api/videos/?page=2

# Page 1, 20 items
GET /api/videos/?page_size=20

# Filter by category
GET /api/videos/by_category/?category=prophecy

# Category with pagination
GET /api/videos/by_category/?category=prophecy&page=2&page_size=15
```

### Prayer Requests
```
GET /api/prayer-requests/
POST /api/prayer-requests/
```

**GET Query Parameters:**
- `page` (optional): Page number
- `page_size` (optional): Items per page

**Example Requests:**
```bash
# First page, default 10 items
GET /api/prayer-requests/

# Page 2, 5 items
GET /api/prayer-requests/?page=2&page_size=5
```

**POST Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "country": "United States",
    "request": "Please pray for my family's health and wellbeing."
}
```

### Course Videos
```
GET /api/course-videos/
```

**Query Parameters:**
- `page` (optional): Page number
- `page_size` (optional): Items per page
- `course_id` (optional): Filter by course ID

**Example Requests:**
```bash
# All course videos, paginated
GET /api/course-videos/

# Videos for specific course
GET /api/course-videos/?course_id=1

# Course videos with pagination
GET /api/course-videos/?course_id=1&page=2&page_size=8
```

### Other Endpoints (All Paginated)

```
GET /api/church-projects/
GET /api/inspiration-quotes/
GET /api/testimonies/
GET /api/upcoming-events/
GET /api/devotions/
GET /api/video-translations/
```

**Example Usage:**
```bash
# Any endpoint supports pagination
GET /api/church-projects/?page=2&page_size=15
GET /api/testimonies/?page=1&page_size=20
```

## Response Format

All paginated responses follow this structure:

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
    ]
}
```

**Response Fields:**
- `count`: Total number of items
- `next`: URL to next page (null if last page)
- `previous`: URL to previous page (null if first page)
- `results`: Array of items for current page

## Frontend Implementation

### Basic Fetch Example
```javascript
async function fetchPaginatedData(endpoint, page = 1, pageSize = 10) {
    const response = await fetch(`${endpoint}?page=${page}&page_size=${pageSize}`);
    return await response.json();
}

// Usage
const videos = await fetchPaginatedData('/api/videos/', 1, 10);
const prayers = await fetchPaginatedData('/api/prayer-requests/', 2, 15);
```

### Pagination Navigation
```javascript
// Handle next page
if (data.next) {
    const nextPageData = await fetch(data.next);
}

// Handle previous page  
if (data.previous) {
    const prevPageData = await fetch(data.previous);
}
```

### React Hook Example
```javascript
function usePaginatedApi(endpoint, initialPageSize = 10) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);

    const fetchData = async (pageNum = 1) => {
        setLoading(true);
        const response = await fetch(`${endpoint}?page=${pageNum}&page_size=${initialPageSize}`);
        const result = await response.json();
        setData(result);
        setPage(pageNum);
        setLoading(false);
    };

    useEffect(() => {
        fetchData(1);
    }, [endpoint]);

    return { data, loading, page, fetchData };
}

// Usage
const { data, loading, page, fetchData } = usePaginatedApi('/api/videos/');
```

## Error Handling

**Common Errors:**
```json
// Invalid page number
{
    "detail": "Invalid page."
}

// Page size too large
{
    "page_size": ["Ensure this value is less than or equal to 100."]
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid parameters)
- `404`: Not found
- `500`: Server error
