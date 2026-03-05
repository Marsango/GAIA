from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-info/', views.current_user, name='current-user'),
    path('sync/usuario/', views.sync_usuario, name='sync-usuario'),
    path('list/usuarios/', views.list_usuarios, name='list-usuarios'),
    path('token/refresh-cookie/', views.refresh_token_from_cookie, name='token-refresh-cookie'),

    # 🔒 Endpoints com segurança progressiva + CAPTCHA
    path('login/cpf/secure/', views.login_with_cpf_secure, name='login-cpf-secure'),
    path('login/cnpj/secure/', views.login_with_cnpj_secure, name='login-cnpj-secure'),
    path('captcha/verify/', views.verify_captcha_endpoint, name='captcha-verify'),

    # Novas rotas
    path('register/', views.register_client_email, name='register-client'),
    path('register/empresa/', views.register_company_email, name='register-company'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),

    path('delete/usuario/', views.delete_usuario, name='delete-usuario'),
    path('delete/usuario/cpf/', views.delete_usuario_by_cpf, name='delete-usuario-cpf'),
    path('delete/usuario/cnpj/', views.delete_usuario_by_cnpj, name='delete-usuario-cnpj'),

    # Sincronização de dados
    path('sync/usuario/cpf/', views.sync_usuario_by_cpf, name='sync-usuario-cpf'),
    path('sync/usuario/cnpj/', views.sync_usuario_by_cnpj, name='sync-usuario-cnpj'),

    path('admin/email-config/', views.manage_email_template, name='email-config'),
    path('test-email/', views.test_send_email, name='test-email'),
]