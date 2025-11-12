import json
import logging
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import DeviceToken
from .serializers import DeviceTokenSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def test_notification(request):
    """
    Test endpoint to send a push notification to all registered devices
    """
    from django.http import JsonResponse
    from django.conf import settings
    
    # Get all device tokens
    tokens = list(DeviceToken.objects.values_list('token', flat=True))
    
    if not tokens:
        return JsonResponse(
            {'status': 'error', 'message': 'No device tokens found'},
            status=400
        )
    
    # Prepare test notification
    title = "Test Notification"
    body = "This is a test notification from the server"
    data = {
        'type': 'test',
        'message': 'Test notification',
        'timestamp': timezone.now().isoformat()
    }
    
    # Send the notification
    result = send_push_notification(
        title=title,
        body=body,
        data=data,
        tokens=tokens
    )
    
    return JsonResponse({
        'status': 'success' if result.get('status') != 'error' else 'error',
        'message': 'Test notification sent',
        'result': result
    })

# Set up logging
logger = logging.getLogger(__name__)

# Expo API endpoint
EXPO_API_URL = 'https://exp.host/--/api/v2/push/send'

@api_view(['POST'])
@permission_classes([AllowAny])
def register_device_token(request):
    """
    Register a new device token or update the last_used timestamp if it exists
    """
    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Received device token registration request")
    
    try:
        serializer = DeviceTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Invalid token data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Received device token: {token}")
        
        # Create or update the device token
        device_token, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={'token': token}
        )
        
        action = "registered" if created else "updated"
        logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully {action} token with ID: {device_token.id}")
        
        return Response(
            {
                'status': 'success', 
                'message': f'Device token {action.lower()} successfully',
                'created': created,
                'token_id': str(device_token.id)
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.exception("[NOTIFICATION] Error in register_device_token")
        return Response(
            {'status': 'error', 'message': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def send_push_notification(title, body, data=None, tokens=None, sound='default'):
    """
    Send push notifications to multiple devices using Expo's Push Notification service
    
    Args:
        title (str): Notification title
        body (str): Notification body
        data (dict, optional): Additional data to send. Defaults to None.
        tokens (list, optional): List of Expo push tokens. If None, sends to all registered devices.
        sound (str, optional): Sound to play when the notification is received. Defaults to 'default'.
    
    Returns:
        dict: Status of the operation with details
    """
    logger = logging.getLogger(__name__)
    
    # Log the notification being sent
    if data and 'devotion_id' in data:
        logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] New devotion created: ID {data['devotion_id']}, Title: \"{data.get('title', 'No title')}\"")
    
    if not tokens:
        # Get all active device tokens if none provided
        tokens = list(DeviceToken.objects.values_list('token', flat=True))
        logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] No tokens provided, using all {len(tokens)} registered tokens")
    
    if not tokens:
        return {'status': 'error', 'message': 'No device tokens available'}
    
    # Filter out any empty or None tokens
    valid_tokens = [token for token in tokens if token]
    if not valid_tokens:
        error_msg = 'No valid device tokens available'
        logger.error(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
        return {'status': 'error', 'message': error_msg}
        
    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(valid_tokens)} valid device tokens to notify")
    
    # Prepare the notification data with platform-specific configurations
    messages = [{
        'to': token,
        'title': title,
        'body': body,
        'sound': sound,
        'data': data or {},
        # Android-specific configuration
        'android': {
            'priority': 'high',
            'channelId': 'default'
        },
        # iOS-specific configuration
        'ios': {
            'sound': sound,
            'badge': 1
        }
    } for token in valid_tokens]
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # Number of retries
        backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
        status_forcelist=[408, 429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["POST"]  # Only retry on POST requests
    )
    
    # Create a session with retry strategy
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    # Set up headers
    headers = {
        'Accept': 'application/json',
        'Accept-encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
    }
    
    # Add Expo access token if available
    if hasattr(settings, 'EXPO_ACCESS_TOKEN') and settings.EXPO_ACCESS_TOKEN:
        headers['Authorization'] = f'Bearer {settings.EXPO_ACCESS_TOKEN}'
    else:
        logger.warning("No EXPO_ACCESS_TOKEN provided. Using unauthenticated mode with lower rate limits.")
    
    # For Android, ensure we're using the correct format
    for message in messages:
        if 'to' in message and message['to']:
            # Ensure the token is in the correct format
            if message['to'].startswith('ExponentPushToken') and not message['to'].startswith('ExponentPushToken['):
                message['to'] = f"ExponentPushToken[{message['to'].replace('ExponentPushToken', '')}]"
    
    success_count = 0
    errors = []
    
    try:
        # Send the notifications in chunks of 100 (Expo's limit)
        chunk_size = 100
        
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i:i + chunk_size]
            
            try:
                logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending to {len(chunk)} tokens...")
                
                # Add a small delay between chunks to avoid rate limiting
                time.sleep(0.5)
                
                # Use the session with retries
                response = session.post(
                    EXPO_API_URL,
                    headers=headers,
                    json=chunk,
                    timeout=10  # 10 seconds timeout
                )
                response_data = response.json() if response.content else {}
                
                if response.status_code == 200:
                    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Expo response: {json.dumps(response_data, indent=2)}")
                    if isinstance(response_data, list):
                        for result in response_data:
                            if result.get('status') == 'error':
                                errors.append({
                                    'token': result.get('details', {}).get('token'),
                                    'message': result.get('message', 'Unknown error'),
                                    'details': result.get('details')
                                })
                            elif result.get('status') == 'ok':
                                success_count += 1
                    elif isinstance(response_data, dict) and 'data' in response_data and isinstance(response_data['data'], list):
                        for result in response_data['data']:
                            if result.get('status') == 'error':
                                errors.append({
                                    'token': result.get('details', {}).get('token'),
                                    'message': result.get('message', 'Unknown error'),
                                    'details': result.get('details')
                                })
                            elif result.get('status') == 'ok':
                                success_count += 1
                else:
                    errors.append({
                        'message': f'Unexpected status code: {response.status_code}',
                        'details': response.text,
                        'status_code': response.status_code
                    })
                    
            except Exception as e:
                error_msg = f'Error sending push notification chunk: {str(e)}'
                logger.exception(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
                errors.append({
                    'message': error_msg,
                    'chunk_size': len(chunk),
                    'tokens': [msg['to'][:10] + '...' for msg in chunk]  # Log first 10 chars of each token
                })
        
        # Log final results
        if data and 'devotion_id' in data:
            if success_count > 0:
                logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully sent notification for devotion {data['devotion_id']} to {success_count} devices")
            if errors:
                error_details = '\n'.join([
                    f"Error {i+1}: {err.get('message')} (Token: {err.get('details', {}).get('token', 'unknown')})"
                    for i, err in enumerate(errors)
                ])
                logger.warning(
                    f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Failed to send {len(errors)} notifications for devotion {data['devotion_id']}\n"
                    f"Error details:\n{error_details}"
                )
        
        # Prepare the response
        result = {
            'status': 'success' if not errors else 'partial',
            'success_count': success_count,
            'error_count': len(errors),
            'total_sent': success_count + len(errors),
            'errors': errors if errors else None,
            'message': f'Sent {success_count} notifications' + (f' with {len(errors)} errors' if errors else '')
        }
        
        if errors:
            result['message'] = f'Sent {success_count} notifications with {len(errors)} errors'
        else:
            result['message'] = f'Successfully sent {success_count} notifications'
        
        return result
        
    except Exception as e:
        logger.exception('Error in send_push_notification')
        return {
            'status': 'error',
            'message': f'Failed to send notifications: {str(e)}',
            'errors': [{'message': str(e)}]
        }
