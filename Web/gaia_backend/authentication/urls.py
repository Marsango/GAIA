from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-info/', views.current_user, name='current-user'),
    path('sync/usuario/', views.sync_usuario, name='sync-usuario'),
    path('list/usuarios/', views.list_usuarios, name='list-usuarios'),
    path('login/cpf/', views.login_with_cpf, name='login-with-cpf'),
    path('login/cnpj/', views.login_with_cnpj, name='login-with-cnpj'),

    # Novas rotas
    path('register/', views.register_client_email, name='register-client'),
    path('register/empresa/', views.register_company_email, name='register-company'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),

    path('delete/usuario/', views.delete_usuario, name='delete-usuario'),

    path('admin/email-config/', views.manage_email_template, name='email-config'),
    path('test-email/', views.test_send_email, name='test-email'),
]