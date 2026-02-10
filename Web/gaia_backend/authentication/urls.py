from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/cpf/', views.login_with_cpf, name='login-with-cpf'),
    path('logout/', views.logout_view, name='logout'),
    path('user-info/', views.current_user, name='current-user'),
    path('sync/usuario/', views.sync_usuario, name='sync-usuario'),

    # Novas rotas
    path('register/', views.register_client_email, name='register-client'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),

    path('admin/email-config/', views.manage_email_template, name='email-config'),
]