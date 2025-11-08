# Application and Authentication Guide

This guide explains how to use the application system for Sons of John Chi and Mentorship programs, including user registration, admin approval, and login functionality.

## Table of Contents
- [1. User Registration](#1-user-registration)
- [2. Admin Approval](#2-admin-approval)
- [3. User Login](#3-user-login)
- [4. Using the API with Authentication](#4-using-the-api-with-authentication)
- [5. Available Endpoints](#5-available-endpoints)
- [6. Error Handling](#6-error-handling)

## 1. User Registration

### Endpoint
```
POST /api/applications/
```

### Request Body
```json
{
    "application_type": "mentorship",  // or "sons_of_john_chi"
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "1234567890",
    "username": "johndoe",
    "password": "securepassword123",
    "your_interest": "I want to learn...",
    "your_goals": "My goals are..."
}
```

### Response (Success)
```json
{
    "id": 1,
    "application_type": "mentorship",
    "status": "pending",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "1234567890",
    "username": "johndoe",
    "your_interest": "I want to learn...",
    "your_goals": "My goals are..."
}
```

## 2. Admin Approval

1. Log in to the Django admin panel at `/admin`
2. Navigate to "Course applications"
3. Find the pending application and click on it
4. Click the "Approve" button to approve the application
   - This will automatically create a user account with the provided credentials

## 3. User Login

### Endpoint
```
POST /api/applications/login/
```

### Request Body
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

### Response (Success)
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    },
    "application_type": "mentorship"
}
```

## 4. Using the API with Authentication

After logging in, include the JWT token in the Authorization header:

```
Authorization: Bearer your_access_token_here
```

### Refreshing Tokens
When the access token expires (default: 5 minutes), use the refresh token to get a new one:

```
POST /api/token/refresh/
```

#### Request Body
```json
{
    "refresh": "your_refresh_token_here"
}
```

#### Response
```json
{
    "access": "new_access_token_here"
}
```

## 5. Available Endpoints

### Public Endpoints
- `POST /api/applications/` - Submit a new application
- `POST /api/applications/login/` - Login with username/password
- `POST /api/token/refresh/` - Refresh access token

### Protected Endpoints (Require Authentication)
- `GET /api/applications/` - List all applications (admin only)
- `GET /api/applications/pending/` - List pending applications (admin only)
- `GET /api/applications/approved/` - List approved applications (admin only)
- `POST /api/applications/{id}/approve/` - Approve an application (admin only)
- `POST /api/applications/{id}/reject/` - Reject an application (admin only)

## 6. Error Handling

### Common Errors

#### Invalid Credentials
```http
HTTP 401 Unauthorized
```
```json
{
    "error": "Invalid credentials"
}
```

#### Username Already Exists
```http
HTTP 400 Bad Request
```
```json
{
    "username": ["This username is already taken."]
}
```

#### Application Already Exists
```http
HTTP 400 Bad Request
```
```json
{
    "email": ["An application for mentorship with this email already exists."]
}
```

#### Missing Required Fields
```http
HTTP 400 Bad Request
```
```json
{
    "field_name": ["This field is required."]
}
```

## Example Usage with cURL

### Register a New Application
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "mentorship",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "1234567890",
    "username": "johndoe",
    "password": "securepassword123",
    "your_interest": "I want to learn...",
    "your_goals": "My goals are..."
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/applications/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepassword123"}'
```

### Make Authenticated Request
```bash
curl http://localhost:8000/api/protected-endpoint/ \
  -H "Authorization: Bearer your_access_token_here"
```
