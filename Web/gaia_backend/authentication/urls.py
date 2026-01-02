from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-info/', views.current_user, name='current-user'),
    path('sync/usuario/', views.sync_usuario, name='sync-usuario'),
]