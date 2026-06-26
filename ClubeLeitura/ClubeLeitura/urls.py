'''
Rotas principais do projeto ClubeLeitura.

Reúne o admin, as rotas de autenticação JWT (SimpleJWT) e a documentação
da API (drf-spectacular). As rotas de documentação recebem
authentication_classes=[] e permission_classes=[AllowAny] porque a permissão
global é IsAuthenticated - sem isso o Swagger/Redoc ficariam bloqueados.
'''
from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps de domínio
    path('livros/', include('livros.urls')),
    path('leituras/', include('leituras.urls')),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Documentação da API (liberada apesar da permissão global IsAuthenticated)
    path('api/schema/', SpectacularAPIView.as_view(
        authentication_classes=[], permission_classes=[AllowAny],
    ), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(
        url_name='schema', authentication_classes=[], permission_classes=[AllowAny],
    ), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(
        url_name='schema', authentication_classes=[], permission_classes=[AllowAny],
    ), name='redoc'),
]
