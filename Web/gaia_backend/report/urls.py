from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropriedadeViewSet, LaudoViewSet, sync_propriedade, sync_laudo

# Cria rotas automáticas para ViewSets
router = DefaultRouter()
router.register(r'propriedades', PropriedadeViewSet)
router.register(r'laudos', LaudoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sync/propriedade/', sync_propriedade, name='sync-propriedade'),
    path('sync/laudo/', sync_laudo, name='sync-laudo'),
]