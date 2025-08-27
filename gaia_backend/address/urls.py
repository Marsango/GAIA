# gaia_backend/address/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet
from person.views import PersonViewSet # <--- IMPORTA A VIEW DE PERSON

router = DefaultRouter()
router.register(r'address', AddressViewSet, basename='address')
router.register(r'person', PersonViewSet, basename='person') # <--- REGISTRAMOS A ROTA DE PERSON AQUI

urlpatterns = router.urls