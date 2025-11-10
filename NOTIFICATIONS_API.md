# Push Notifications API Documentation

This document outlines how to integrate with the push notification system for the Ark of God mobile app.

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Endpoints](#endpoints)
  - [Register Device Token](#register-device-token)
  - [Sending Notifications](#sending-notifications)
- [Mobile Integration](#mobile-integration)
- [Troubleshooting](#troubleshooting)

## Overview
The push notification system allows the server to send real-time notifications to mobile devices using Expo's push notification service. The system is designed to work with the Expo React Native client.

## Setup
1. Ensure your mobile app has the required Expo Notifications permissions
2. Install the necessary dependencies in your React Native app:
   ```bash
   expo install expo-notifications
   ```
3. The backend is already configured to handle push notifications through the Expo service.

## Endpoints

### Register Device Token

#### `POST /api/notifications/register-device/`

Registers a device's Expo push token with the server to receive push notifications.

**Request Body:**
```json
{
  "token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
}
```

**Response:**
- `201 Created` on successful registration
- `400 Bad Request` if the token is invalid

**Example Response (201):**
```json
{
  "status": "success",
  "message": "Device token registered successfully"
}
```

## Sending Notifications

### Automatic Notifications
Notifications are automatically sent in the following scenarios:
- When a new devotion is created

### Manual Notification Sending
You can manually trigger notifications by calling the `send_push_notification` function from anywhere in the Django codebase:

```python
from notifications.views import send_push_notification

# Send a basic notification
result = send_push_notification(
    title="Notification Title",
    body="This is the notification message",
    data={"key": "value"},  # Optional custom data
    sound="default"  # Sound to play (default: 'default')
)

# Send to specific tokens
result = send_push_notification(
    title="Specific Users",
    body="This goes to specific devices",
    tokens=["token1", "token2"]  # List of Expo push tokens
)
```

## Mobile Integration

### Requesting Permissions
```javascript
import * as Notifications from 'expo-notifications';

async function registerForPushNotifications() {
  // Request permission
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;
  
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }
  
  if (finalStatus !== 'granted') {
    console.log('Failed to get push token for push notification!');
    return;
  }
  
  // Get the token
  const token = (await Notifications.getExpoPushTokenAsync()).data;
  
  // Register with your backend
  await registerDeviceToken(token);
}

async function registerDeviceToken(token) {
  try {
    const response = await fetch('YOUR_BACKEND_URL/api/notifications/register-device/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token }),
    });
    
    const data = await response.json();
    console.log('Device token registration:', data);
  } catch (error) {
    console.error('Error registering device token:', error);
  }
}
```

### Handling Received Notifications
```javascript
import * as Notifications from 'expo-notifications';

// Configure how notifications are handled when the app is in the foreground
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// Listen for notification events
const subscription = Notifications.addNotificationReceivedListener(notification => {
  console.log('Notification received:', notification);
  // Handle the notification
  const { title, body, data } = notification.request.content;
  
  // Example: Navigate to a specific screen based on the notification data
  if (data && data.type === 'new_devotion') {
    navigation.navigate('Devotion', { devotionId: data.devotion_id });
  }
});

// Clean up the listener when component unmounts
return () => {
  Notifications.removeNotificationSubscription(subscription);
};
```

## Troubleshooting

### Common Issues

#### Notifications not received
1. Verify the device token is correctly registered with the server
2. Check the server logs for any errors when sending notifications
3. Ensure the mobile app has notification permissions enabled
4. Verify the Expo push token is valid and not expired

#### Server Errors
- Check the server logs for detailed error messages
- Verify the Expo API endpoint is accessible from your server
- Ensure the server has internet access to reach Expo's push notification service

### Testing Notifications
You can test the notification system using the Expo Push Notification Tool:
1. Get your Expo push token from the mobile app logs
2. Use the token to send a test notification using the `send_push_notification` function
3. Check the mobile device for the test notification

## Rate Limiting and Quotas
- The system respects Expo's rate limits (100 notifications per second)
- Notifications are automatically chunked to comply with these limits
- Monitor your Expo account for any usage quotas

## Security Considerations
- The registration endpoint is currently open (no authentication required)
- In production, consider adding rate limiting or authentication
- Do not expose sensitive information in notification data as it's not encrypted
