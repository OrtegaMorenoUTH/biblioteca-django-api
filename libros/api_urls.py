from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from . import api_views
from .jwt_views import CustomTokenObtainPairView
from . import oauth_views 

# ===== ROUTER =====
router = DefaultRouter()
router.register(r'libros', api_views.LibroViewSet, basename='libro')
router.register(r'autores', api_views.AutorViewSet, basename='autor')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'prestamos', api_views.PrestamoViewSet, basename='prestamo')

# ===== URLS =====
urlpatterns = [
    # 🔐 JWT
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ─────────────────────────────────
    # 🔑 AUTENTICACIÓN OAUTH 2.0 (GOOGLE)
    # ─────────────────────────────────
    path('auth/google/redirect/', oauth_views.google_oauth_redirect, name='google_redirect'),
    path('auth/google/callback/', oauth_views.google_oauth_callback, name='google_callback'),
    
    # 📚 API
    path('', include(router.urls)),
]