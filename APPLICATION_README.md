# Course Applications API - Complete Documentation

## Overview

The Course Applications API allows users to apply for **Sons of John Chi** or **Mentorship** courses. Users create an account during application submission, and admins can approve or reject applications. Once approved, users can log in with their credentials.

## Features

- **Two Application Types**: Sons of John Chi and Mentorship
- **Application Status**: Pending, Approved, or Rejected
- **User Account Creation**: Automatic account creation upon approval
- **Immediate Login**: Users can log in with their credentials even while pending
- **Admin Review**: Admins can approve/reject applications via API or admin panel
- **Bulk Actions**: Admin panel supports bulk approve/reject
- **Filtering**: Filter by application type and status

---

## Table of Contents

1. [Application Flow](#application-flow)
2. [Authentication](#authentication)
3. [Application Model](#application-model)
4. [API Endpoints](#api-endpoints)
5. [Usage Examples](#usage-examples)
6. [Error Handling](#error-handling)

---

## Application Flow

```
1. User submits application (no auth required)
   ↓
2. Application status = "pending"
   ↓
3. User can login with username/password (even while pending)
   ↓
4. Admin reviews application
   ↓
5. Admin approves → User account created, status = "approved"
   OR
   Admin rejects → status = "rejected"
   ↓
6. User continues to access app with full privileges (if approved)
```

---

## Authentication

### For Applicants

Users can log in immediately after submitting their application, even while it's pending:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_applicant",
    "password": "secure_password123"
  }'
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 5,
    "username": "john_applicant",
    "email": "john@example.com",
    "country": "",
    "contact": "+1234567890"
  }
}
```

### For Admins

Admins need to log in to review applications:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin_password"
  }'
```

Save the token:
```bash
export TOKEN="your_admin_token_here"
```

---

## Application Model

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Auto | Unique identifier |
| `application_type` | String | Yes | `sons_of_john_chi` or `mentorship` |
| `status` | String | Auto | `pending`, `approved`, or `rejected` (default: `pending`) |
| `full_name` | String | Yes | Applicant's full name |
| `email` | Email | Yes | Applicant's email (must be unique) |
| `phone_number` | String | Yes | Applicant's phone number |
| `your_interest` | Text | Yes | Why interested in the course |
| `your_goals` | Text | Yes | Applicant's goals |
| `username` | String | Yes | Desired username (must be unique) |
| `password` | String | Yes | Password (will be hashed) |
| `user` | ForeignKey | Auto | Linked user account (created on approval) |
| `created_at` | DateTime | Auto | Application submission date |
| `updated_at` | DateTime | Auto | Last update date |
| `reviewed_at` | DateTime | Auto | Review date |
| `reviewed_by` | ForeignKey | Auto | Admin who reviewed |

### Application Types
- **`sons_of_john_chi`**: Sons of John Chi course
- **`mentorship`**: Mentorship program

### Status Options
- **`pending`**: Application submitted, awaiting review
- **`approved`**: Application approved, user account created
- **`rejected`**: Application rejected

---

## API Endpoints

### 1. Submit Application (Public)

- **URL**: `/api/applications/`
- **Method**: `POST`
- **Permission**: AllowAny (no authentication required)
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "application_type": "sons_of_john_chi",
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone_number": "+1234567890",
  "your_interest": "I am passionate about learning more about spiritual growth and want to deepen my understanding of biblical principles.",
  "your_goals": "My goal is to become a better leader in my community and help others grow in their faith journey.",
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "mentorship",
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone_number": "+9876543210",
    "your_interest": "I want to be mentored in ministry and leadership",
    "your_goals": "To develop my gifts and serve effectively in ministry",
    "username": "jane_smith",
    "password": "MyPassword456!"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "application_type": "mentorship",
  "status": "pending",
  "full_name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone_number": "+9876543210",
  "your_interest": "I want to be mentored in ministry and leadership",
  "your_goals": "To develop my gifts and serve effectively in ministry",
  "username": "jane_smith",
  "user": null,
  "user_details": null,
  "created_at": "2025-11-07T12:00:00Z",
  "updated_at": "2025-11-07T12:00:00Z",
  "reviewed_at": null,
  "reviewed_by": null
}
```

### 2. List All Applications (Admin Only)

- **URL**: `/api/applications/`
- **Method**: `GET`
- **Permission**: IsAdminUser
- **Query Parameters**:
  - `application_type` (optional): Filter by `sons_of_john_chi` or `mentorship`
  - `status` (optional): Filter by `pending`, `approved`, or `rejected`

**cURL Example:**
```bash
# Get all applications
curl http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer $TOKEN"

# Get only pending applications
curl http://localhost:8000/api/applications/?status=pending \
  -H "Authorization: Bearer $TOKEN"

# Get Sons of John Chi applications
curl http://localhost:8000/api/applications/?application_type=sons_of_john_chi \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "application_type": "mentorship",
    "status": "pending",
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone_number": "+9876543210",
    "your_interest": "I want to be mentored in ministry and leadership",
    "your_goals": "To develop my gifts and serve effectively in ministry",
    "username": "jane_smith",
    "user": null,
    "user_details": null,
    "created_at": "2025-11-07T12:00:00Z",
    "updated_at": "2025-11-07T12:00:00Z",
    "reviewed_at": null,
    "reviewed_by": null
  }
]
```

### 3. Get Pending Applications (Admin Only)

- **URL**: `/api/applications/pending/`
- **Method**: `GET`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl http://localhost:8000/api/applications/pending/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Get Approved Applications (Admin Only)

- **URL**: `/api/applications/approved/`
- **Method**: `GET`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl http://localhost:8000/api/applications/approved/ \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get Single Application (Admin Only)

- **URL**: `/api/applications/{id}/`
- **Method**: `GET`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl http://localhost:8000/api/applications/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Approve Application (Admin Only)

- **URL**: `/api/applications/{id}/approve/`
- **Method**: `POST`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/applications/1/approve/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "detail": "Application approved successfully",
  "application": {
    "id": 1,
    "application_type": "mentorship",
    "status": "approved",
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone_number": "+9876543210",
    "your_interest": "I want to be mentored in ministry and leadership",
    "your_goals": "To develop my gifts and serve effectively in ministry",
    "username": "jane_smith",
    "user": 5,
    "user_details": {
      "id": 5,
      "username": "jane_smith",
      "email": "jane.smith@example.com",
      "country": "",
      "contact": "+9876543210"
    },
    "created_at": "2025-11-07T12:00:00Z",
    "updated_at": "2025-11-07T12:30:00Z",
    "reviewed_at": "2025-11-07T12:30:00Z",
    "reviewed_by": 1
  }
}
```

### 7. Reject Application (Admin Only)

- **URL**: `/api/applications/{id}/reject/`
- **Method**: `POST`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/applications/1/reject/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "detail": "Application rejected",
  "application": {
    "id": 1,
    "application_type": "mentorship",
    "status": "rejected",
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone_number": "+9876543210",
    "your_interest": "I want to be mentored in ministry and leadership",
    "your_goals": "To develop my gifts and serve effectively in ministry",
    "username": "jane_smith",
    "user": null,
    "user_details": null,
    "created_at": "2025-11-07T12:00:00Z",
    "updated_at": "2025-11-07T12:35:00Z",
    "reviewed_at": "2025-11-07T12:35:00Z",
    "reviewed_by": 1
  }
}
```

### 8. Delete Application (Admin Only)

- **URL**: `/api/applications/{id}/`
- **Method**: `DELETE`
- **Permission**: IsAdminUser

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/applications/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
*Status: 204 No Content*

---

## Usage Examples

### Scenario 1: User Applies for Sons of John Chi

```bash
# Step 1: User submits application (no auth required)
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "sons_of_john_chi",
    "full_name": "Michael Johnson",
    "email": "michael.j@example.com",
    "phone_number": "+1555123456",
    "your_interest": "I have been following the teachings and want to join the Sons of John Chi community to grow spiritually",
    "your_goals": "To understand biblical prophecy better and serve in ministry",
    "username": "michael_j",
    "password": "MySecurePass789!"
  }'

# Step 2: User can immediately login (even while pending)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "michael_j",
    "password": "MySecurePass789!"
  }'

# User receives token and can access the app
```

### Scenario 2: Admin Reviews and Approves Application

```bash
# Step 1: Admin logs in
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

export TOKEN="admin_token_here"

# Step 2: Admin views pending applications
curl http://localhost:8000/api/applications/pending/ \
  -H "Authorization: Bearer $TOKEN"

# Step 3: Admin reviews specific application
curl http://localhost:8000/api/applications/5/ \
  -H "Authorization: Bearer $TOKEN"

# Step 4: Admin approves application
curl -X POST http://localhost:8000/api/applications/5/approve/ \
  -H "Authorization: Bearer $TOKEN"

# User account is now created and application is approved
```

### Scenario 3: Admin Rejects Application

```bash
# Admin logs in
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

export TOKEN="admin_token_here"

# Admin rejects application
curl -X POST http://localhost:8000/api/applications/6/reject/ \
  -H "Authorization: Bearer $TOKEN"

# Application status changed to "rejected"
```

### Scenario 4: User Applies for Mentorship

```bash
# Submit mentorship application
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "mentorship",
    "full_name": "Sarah Williams",
    "email": "sarah.w@example.com",
    "phone_number": "+1555987654",
    "your_interest": "I am seeking mentorship to develop my leadership skills and ministry calling",
    "your_goals": "To become an effective leader and mentor others in their faith journey",
    "username": "sarah_w",
    "password": "SecurePass321!"
  }'

# User logs in
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah_w",
    "password": "SecurePass321!"
  }'
```

### Scenario 5: User Applies for Both Courses

```bash
# Step 1: Apply for Sons of John Chi
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "sons_of_john_chi",
    "full_name": "David Brown",
    "email": "david.b@example.com",
    "phone_number": "+1555246810",
    "your_interest": "I want to join Sons of John Chi to grow spiritually",
    "your_goals": "To understand biblical prophecy and serve in ministry",
    "username": "david_b_sojc",
    "password": "SecurePass111!"
  }'

# Step 2: Same user applies for Mentorship (same email, different username)
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "mentorship",
    "full_name": "David Brown",
    "email": "david.b@example.com",
    "phone_number": "+1555246810",
    "your_interest": "I also want mentorship to develop leadership skills",
    "your_goals": "To become an effective leader and mentor others",
    "username": "david_b_mentor",
    "password": "SecurePass222!"
  }'

# Both applications submitted successfully with the same email!
```

### Scenario 6: Filtering Applications

```bash
# Get all Sons of John Chi applications
curl http://localhost:8000/api/applications/?application_type=sons_of_john_chi \
  -H "Authorization: Bearer $TOKEN"

# Get all approved mentorship applications
curl "http://localhost:8000/api/applications/?application_type=mentorship&status=approved" \
  -H "Authorization: Bearer $TOKEN"

# Get all rejected applications
curl http://localhost:8000/api/applications/?status=rejected \
  -H "Authorization: Bearer $TOKEN"
```

---

## Error Handling

### Common Errors

#### 1. Duplicate Username

**Request:**
```json
{
  "username": "existing_user",
  ...
}
```

**Response (400 Bad Request):**
```json
{
  "username": [
    "This username is already taken."
  ]
}
```

#### 2. Duplicate Email for Same Application Type

**Note**: The same email can apply for both Sons of John Chi and Mentorship, but cannot submit multiple applications for the same type.

**Request:**
```json
{
  "email": "existing@example.com",
  "application_type": "sons_of_john_chi"
  ...
}
```

**Response (400 Bad Request - if already applied for this type):**
```json
{
  "email": [
    "An application for sons_of_john_chi with this email already exists. You can apply for the other course type."
  ]
}
```

#### 3. Missing Required Fields

**Response (400 Bad Request):**
```json
{
  "full_name": ["This field is required."],
  "email": ["This field is required."],
  "your_interest": ["This field is required."]
}
```

#### 4. Invalid Application Type

**Response (400 Bad Request):**
```json
{
  "application_type": [
    "\"invalid_type\" is not a valid choice."
  ]
}
```

#### 5. Already Reviewed Application

**Response (400 Bad Request):**
```json
{
  "detail": "Application is already approved"
}
```

#### 6. Unauthorized Access (Non-Admin)

**Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Permissions Summary

| Action | Endpoint | Permission Required |
|--------|----------|---------------------|
| Submit application | `POST /api/applications/` | None (Public) |
| List applications | `GET /api/applications/` | Admin |
| Get single application | `GET /api/applications/{id}/` | Admin |
| Approve application | `POST /api/applications/{id}/approve/` | Admin |
| Reject application | `POST /api/applications/{id}/reject/` | Admin |
| Delete application | `DELETE /api/applications/{id}/` | Admin |
| Get pending applications | `GET /api/applications/pending/` | Admin |
| Get approved applications | `GET /api/applications/approved/` | Admin |

---

## Admin Panel Features

### Bulk Actions

Admins can select multiple applications and:
- **Approve Selected**: Bulk approve multiple pending applications
- **Reject Selected**: Bulk reject multiple pending applications

### Filters

- Filter by application type (Sons of John Chi / Mentorship)
- Filter by status (Pending / Approved / Rejected)
- Date hierarchy by creation date

### Search

Search by:
- Full name
- Email
- Username
- Phone number

---

## Best Practices

### For Applicants

1. **Strong Passwords**: Use secure passwords with letters, numbers, and symbols
2. **Valid Email**: Provide a valid email address for communication
3. **Multiple Applications**: You can apply for both Sons of John Chi and Mentorship with the same email
4. **Unique Username**: Choose a unique username not already taken (must be different for each application)
5. **Detailed Responses**: Provide thoughtful answers for interest and goals
6. **Accurate Information**: Ensure all information is correct before submitting

### For Admins

1. **Timely Review**: Review applications promptly to avoid delays
2. **Bulk Actions**: Use bulk approve/reject for efficiency
3. **Communication**: Contact applicants if more information is needed
4. **Record Keeping**: Applications are preserved even after approval/rejection
5. **Fair Review**: Review all applications fairly and consistently

### For Developers

1. **Password Security**: Passwords are automatically hashed before storage
2. **Validation**: Username and email uniqueness is enforced
3. **Status Tracking**: Monitor application status changes
4. **Error Handling**: Handle duplicate username/email gracefully
5. **User Experience**: Provide clear feedback on application status

---

## Integration Examples

### React/React Native Example

```javascript
// Submit application
const submitApplication = async (applicationData) => {
  try {
    const response = await fetch('http://localhost:8000/api/applications/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(applicationData)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('Application submitted:', data);
      
      // User can now login immediately
      return data;
    } else {
      const errors = await response.json();
      console.error('Application errors:', errors);
      throw errors;
    }
  } catch (error) {
    console.error('Error submitting application:', error);
    throw error;
  }
};

// Login after application
const loginAfterApplication = async (username, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store token
      localStorage.setItem('token', data.token);
      localStorage.setItem('refresh', data.refresh);
      return data;
    } else {
      throw new Error('Login failed');
    }
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

// Admin: Approve application
const approveApplication = async (applicationId, token) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/applications/${applicationId}/approve/`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error approving application:', error);
    throw error;
  }
};

// Admin: Get pending applications
const getPendingApplications = async (token) => {
  try {
    const response = await fetch('http://localhost:8000/api/applications/pending/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching applications:', error);
    throw error;
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

This will create the `CourseApplication` table in your database.

---

## Quick Reference

### Application Types
- `sons_of_john_chi` - Sons of John Chi course
- `mentorship` - Mentorship program

### Status Values
- `pending` - Awaiting admin review
- `approved` - Approved, user account created
- `rejected` - Application rejected

### Special Endpoints
- `/api/applications/pending/` - Get pending applications
- `/api/applications/approved/` - Get approved applications
- `/api/applications/{id}/approve/` - Approve application
- `/api/applications/{id}/reject/` - Reject application

---

## Support

For issues or questions about the Applications API, contact your development team or refer to the main API documentation.
