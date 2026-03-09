from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlencode
import urllib.parse
import requests
import logging
from django.shortcuts import redirect
import json

logger = logging.getLogger(__name__)
User = get_user_model()



@api_view(['POST', 'GET'])  # ← AGREGAR SOPORTE PARA GET
@permission_classes([AllowAny])
def google_oauth_callback(request):
    """
    Endpoint que recibe el código de autorización de Google
    y devuelve tokens JWT de nuestra aplicación
    
    GET /api/auth/google/callback/?code=4/0AbUR2VN...
    o
    POST /api/auth/google/callback/
    Body: {
        "code": "4/0AbUR2VN..."  // Código de autorización de Google
    }
    """
    code = request.GET.get('code')
    print(f"📥 Code recibido: {code}")  # Debug
    
    if not code:
        return Response({'error': 'No code provided'}, status=400)
    
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
        'client_secret': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
        'redirect_uri': 'http://127.0.0.1:8000/api/auth/google/callback/',  # ✅ USAR 127.0.0.1
        'grant_type': 'authorization_code',
    }
    
    try:
        # 2. Intercambiar código por access token de Google
        token_url = 'https://oauth2.googleapis.com/token'
        
        google_config = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']
        
        token_data = {
            'code': code,
            'client_id': google_config['client_id'],
            'client_secret': google_config['secret'],
            'redirect_uri': 'http://127.0.0.1:8000/api/auth/google/callback/',  # Debe coincidir con Google Cloud
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data, timeout=10)
        token_response.raise_for_status()
        
        tokens = token_response.json()
        google_access_token = tokens.get('access_token')
        
        if not google_access_token:
            error_msg = 'No se pudo obtener access token de Google'
            logger.error(error_msg)
            return redirect(f'/oauth/login/?error={urllib.parse.quote(error_msg)}')
        
        logger.info(f"Access token de Google obtenido: {google_access_token[:20]}...")
        
        # 3. Obtener información del usuario de Google
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {google_access_token}'}
        
        userinfo_response = requests.get(userinfo_url, headers=headers, timeout=10)
        userinfo_response.raise_for_status()
        
        user_data = userinfo_response.json()
        
        logger.info(f"Datos de usuario de Google: {user_data}")
        
        # 4. Crear o actualizar usuario en Django
        email = user_data.get('email')
        
        if not email:
            error_msg = 'No se pudo obtener el email del usuario'
            logger.error(error_msg)
            return redirect(f'/oauth/login/?error={urllib.parse.quote(error_msg)}')
        
        # Buscar si el usuario ya existe
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],  # Usar parte antes del @ como username
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', ''),
            }
        )
        
        # Si el usuario ya existía, actualizar su información
        if not created:
            user.first_name = user_data.get('given_name', user.first_name)
            user.last_name = user_data.get('family_name', user.last_name)
            user.save()
            logger.info(f"Usuario existente actualizado: {user.email}")
        else:
            logger.info(f"Nuevo usuario creado: {user.email}")
        
        # 5. Generar tokens JWT de nuestra aplicación
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # 6. Preparar datos para enviar al frontend
        user_info = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
        }
        
        google_info = {
            'picture': user_data.get('picture'),
            'verified_email': user_data.get('verified_email'),
        }
        
        # Codificar datos para URL
        user_info_json = json.dumps(user_info)
        google_info_json = json.dumps(google_info)
        
        # Construir URL de redirección a oauth_login.html con todos los datos
        redirect_url = (
            f'/oauth/login/?'
            f'access_token={access_token}&'
            f'refresh_token={str(refresh)}&'
            f'user_info={urllib.parse.quote(user_info_json)}&'
            f'google_info={urllib.parse.quote(google_info_json)}&'
            f'message={urllib.parse.quote("Login exitoso con Google" if not created else "Cuenta creada exitosamente con Google")}'
        )
        
        logger.info(f"Redirigiendo a: {redirect_url[:100]}...")
        return redirect(redirect_url)
    
    except requests.Timeout:
        logger.error("Timeout al comunicarse con Google")
        return redirect(f'/oauth/login/?error={urllib.parse.quote("Timeout al comunicarse con Google")}')
    
    except requests.RequestException as e:
        logger.error(f"Error al comunicarse con Google: {str(e)}")
        return redirect(f'/oauth/login/?error={urllib.parse.quote(f"Error con Google: {str(e)}")}')
    
    except Exception as e:
        logger.error(f"Error inesperado en OAuth: {str(e)}")
        return redirect(f'/oauth/login/?error={urllib.parse.quote(f"Error inesperado: {str(e)}")}')

    return redirect(
    f'/oauth/login/?access={jwt_token}&refresh={refresh_token}'
    f'&email={user_info.get("email")}&username={user.username}'
)

@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_redirect(request):
    """
    Endpoint que redirige al usuario a Google para autorización
    
    GET /api/auth/google/redirect/
    
    Devuelve la URL a la que el frontend debe redirigir al usuario
    """
    
    google_config = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']
    scopes = settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE']
    
    # Construir parámetros como diccionario para usar urlencode
    params = {
        'client_id': google_config["client_id"],
        'redirect_uri': 'http://127.0.0.1:8000/api/auth/google/callback/',
        'scope': " ".join(scopes),
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    
    # Construir URL con urlencode para codificar correctamente los parámetros
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'  # ← USAR URLENCODE
    
    return Response({
        'auth_url': auth_url
    }, status=status.HTTP_200_OK)