from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-info/', views.user_info, name='user-info'),
    path('sync/usuario/', views.sync_usuario, name='sync-usuario'),
]