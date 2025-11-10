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
    if not tokens:
        # Get all active device tokens if none provided
        tokens = list(DeviceToken.objects.values_list('token', flat=True))
    
    if not tokens:
        return {'status': 'error', 'message': 'No device tokens available'}
    
    # Filter out any empty or None tokens
    valid_tokens = [token for token in tokens if token]
    if not valid_tokens:
        return {'status': 'error', 'message': 'No valid device tokens available'}
    
    # Prepare the notification data
    messages = [{
        'to': token,
        'title': title,
        'body': body,
        'sound': sound,
        'data': data or {}
    } for token in valid_tokens]
    
    # Send the notifications
    headers = {
        'Accept': 'application/json',
        'Accept-encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
    }
    
    success_count = 0
    errors = []
    
    try:
        # Send the notifications in chunks of 100 (Expo's limit)
        chunk_size = 100
        
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i:i + chunk_size]
            
            try:
                response = requests.post(EXPO_API_URL, headers=headers, json=chunk)
                response_data = response.json()
                
                if response.status_code == 200:
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
                logger.exception('Error sending push notification chunk')
                errors.append({'message': str(e)})
        
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
