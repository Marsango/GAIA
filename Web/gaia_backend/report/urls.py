from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropriedadeViewSet, LaudoViewSet

# Cria rotas automáticas para ViewSets
router = DefaultRouter()
router.register(r'propriedades', PropriedadeViewSet)
router.register(r'laudos', LaudoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]