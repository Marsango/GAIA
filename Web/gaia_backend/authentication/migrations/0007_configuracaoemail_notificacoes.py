# Generated migration for notification email templates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_configuracaoemail_mensagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaoemail',
            name='assunto_mudanca_login',
            field=models.CharField(
                blank=True,
                default='GAIA - Seu Login foi Atualizado',
                max_length=200
            ),
        ),
        migrations.AddField(
            model_name='configuracaoemail',
            name='mensagem_mudanca_login',
            field=models.TextField(
                blank=True,
                default="""Olá {nome},

Informamos que o login para acessar o sistema GAIA foi atualizado.

Seu novo login é:
{novo_login}

Se você não realizou esta alteração, entre em contato imediatamente com nosso suporte.

Att,
Equipe GAIA"""
            ),
        ),
        migrations.AddField(
            model_name='configuracaoemail',
            name='assunto_mudanca_email',
            field=models.CharField(
                blank=True,
                default='GAIA - Seu E-mail foi Atualizado',
                max_length=200
            ),
        ),
        migrations.AddField(
            model_name='configuracaoemail',
            name='mensagem_mudanca_email',
            field=models.TextField(
                blank=True,
                default="""Olá {nome},

Confirmamos que o e-mail da sua conta no sistema GAIA foi atualizado com sucesso.

Seu novo e-mail de acesso é:
{novo_email}

Se você não realizou esta alteração, entre em contato imediatamente com nosso suporte.

Att,
Equipe GAIA"""
            ),
        ),
    ]
