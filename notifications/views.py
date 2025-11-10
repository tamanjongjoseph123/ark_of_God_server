import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import DeviceToken
from .serializers import DeviceTokenSerializer

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
    logger.info("[NOTIFICATION] Received device token registration request")
    
    try:
        logger.debug(f"[NOTIFICATION] Request data: {request.data}")
        serializer = DeviceTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"[NOTIFICATION] Invalid token data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        logger.info(f"[NOTIFICATION] Processing token: {token[:10]}...")
        
        # Create or update the device token
        device_token, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={'token': token}
        )
        
        action = "Registered" if created else "Updated"
        logger.info(f"[NOTIFICATION] Successfully {action.lower()} device token: {token[:10]}...")
        
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
    logger.info(f"[NOTIFICATION] Starting to send notification. Title: {title}, Body: {body}")
    
    if not tokens:
        logger.info("[NOTIFICATION] No tokens provided, fetching all registered device tokens")
        # Get all active device tokens if none provided
        tokens = list(DeviceToken.objects.values_list('token', flat=True))
    
    logger.info(f"[NOTIFICATION] Found {len(tokens)} device tokens")
    
    if not tokens:
        error_msg = 'No device tokens available'
        logger.error(f"[NOTIFICATION] {error_msg}")
        return {'status': 'error', 'message': error_msg}
    
    # Filter out any empty or None tokens
    valid_tokens = [token for token in tokens if token]
    logger.info(f"[NOTIFICATION] {len(valid_tokens)} valid tokens after filtering")
    
    if not valid_tokens:
        error_msg = 'No valid device tokens available after filtering'
        logger.error(f"[NOTIFICATION] {error_msg}")
        return {'status': 'error', 'message': error_msg}
    
    # Prepare the notification data
    messages = []
    for token in valid_tokens:
        message = {
            'to': token,
            'title': title,
            'body': body,
            'sound': sound,
            'data': data or {}
        }
        messages.append(message)
    
    # Send the notifications
    headers = {
        'Accept': 'application/json',
        'Accept-encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
    }
    
    try:
        logger.info("[NOTIFICATION] Sending notifications to Expo's push service")
        # Send the notifications in chunks of 100 (Expo's limit)
        chunk_size = 100
        success_count = 0
        errors = []
        
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i:i + chunk_size]
            chunk_num = (i // chunk_size) + 1
            logger.info(f"[NOTIFICATION] Processing chunk {chunk_num} with {len(chunk)} messages")
            
            try:
                response = requests.post(
                    EXPO_API_URL,
                    headers=headers,
                    json=chunk
                )
                
                response_data = response.json()
                
                # Check for errors in the response
                if response.status_code == 200 and isinstance(response_data, list):
                    for result in response_data:
                        if result.get('status') == 'error':
                            errors.append({
                                'token': result.get('details', {}).get('token'),
                                'message': result.get('message', 'Unknown error'),
                                'details': result.get('details')
                            })
                        else:
                            success_count += 1
                else:
                    errors.append({
                        'message': f'Unexpected response: {response.status_code}',
                        'details': response.text
                    })
                    
            except Exception as e:
                logger.exception(f'Error sending push notification chunk {i//chunk_size + 1}')
                errors.append({
                    'message': str(e),
                    'chunk': i // chunk_size + 1
                })
        
        # Prepare the response
        result = {
            'status': 'success' if not errors or success_count > 0 else 'error',
            'success_count': success_count,
            'error_count': len(errors),
            'total_sent': success_count + len(errors),
            'errors': errors if errors else None
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
