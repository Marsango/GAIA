# report/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'propriedades', views.PropriedadeViewSet, basename='propriedade')
router.register(r'laudos', views.LaudoViewSet, basename='laudo')
router.register(r'amostras', views.AmostraViewSet, basename='amostra')
router.register(r'empresas', views.EmpresaViewSet, basename='empresa')
router.register(r'pessoas', views.PersonViewSet, basename='person')
router.register(r'enderecos', views.EnderecoViewSet, basename='endereco')

urlpatterns = [
     # Info pública
     path('info/', views.api_info, name='api-info'),
     
     # API via router
     path('', include(router.urls)),
    
     path('health/', views.health_check, name='health-check'),
     path('usuarios/me/', views.current_user, name='current-user'),
     path('empres/', views.EmpresaViewSet.as_view({'get': 'list', 'post': 'create'}), name='empresa-list'),
]