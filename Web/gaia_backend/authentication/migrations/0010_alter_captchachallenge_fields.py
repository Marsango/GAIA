# Generated migration to fix CAPTCHA field length issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_configuracaoemail_mensagem_captchachallenge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captchachallenge',
            name='challenge_key',
            field=models.CharField(max_length=50),  # Increased from 10 to 50
        ),
        migrations.AlterField(
            model_name='captchachallenge',
            name='correct_answer',
            field=models.CharField(max_length=20),  # Increased from 10 to 20
        ),
    ]
