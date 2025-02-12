from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import AbstractUser

# Models de imagem de usuário customizada
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        # Pasta no servidor onde as imagens serão salvas.
        upload_to='profile_pictures/',
        # Caminho para a imagem padrão que será usada se o usuário não carregar uma.
        default='default_profile/default-avatar.jpg',
        # Permite que o campo fique vazio durante a criação do usuário.
        blank=True
    )

# Models de tarefas
class Lista_tarefas(models.Model):

    STATUS = (
        ('Fazendo', 'fazendo'),
        ('Feito', 'feito'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    done = models.CharField(max_length=7, choices=STATUS, default='Fazendo')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    #on_delete=models.CASCADE = se o usuário for deletado, as tarefas dele também serão deletadas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Método para retornar o título da tarefa
    def __str__(self):
        return self.title

# Models de tokens para recuperação de senha
class password_reset_token(models.Model):

    # Relaciona o token ao usuário que requisitou.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Armazena o token gerado para recuperação de senha (Único para cada usuário.)
    token = models.CharField(max_length=64, unique=True)

    # Armazena a data de criação do token (Útil para verificar a expiração.)
    created_at = models.DateTimeField(auto_now_add=True)

    # Armazena se o token foi utilizado (Garante que cada token seja utilizado uma única vez.)
    is_used = models.BooleanField(default=False)

    #   Valida se o token ainda é utilizável:
    # - Não está expirado (válido por 1 hora).
    # - Ainda não foi usado.
    def is_valid(self):

        # Define o tempo de expiração (ex.: 1 hora)
        expiration_time = self.created_at + timedelta(hours=1)

        # Obtém o tempo atual
        current_time = datetime.now(timezone.utc)
        # Retorna se o token é válido ou não (True/False)
        return not self.is_used and expiration_time > current_time
    
    def __str__(self):
        return f"Token for {self.user.username}"