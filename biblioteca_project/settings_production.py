from .settings import *

# Configuración de producción
DEBUG = False

ALLOWED_HOSTS = [
    'tuusername.pythonanywhere.com',  # Reemplaza con tu username
    'localhost',
    '127.0.0.1',
]

# Base de datos MySQL de PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tuusername$biblioteca',  # Reemplaza con tu username
        'USER': 'tuusername',  # Tu username de PythonAnywhere
        'PASSWORD': 'tu_password_mysql',  # La crearás en PythonAnywhere
        'HOST': 'tuusername.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Archivos estáticos (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Middleware para servir archivos estáticos
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuración de seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# CORS (ajustar según necesites)
CORS_ALLOWED_ORIGINS = [
    'https://tuusername.pythonanywhere.com',
]

# OAuth redirect URIs para producción
# Actualiza oauth_views.py para usar esta variable
OAUTH_REDIRECT_URI = 'https://tuusername.pythonanywhere.com/api/auth/google/callback/'