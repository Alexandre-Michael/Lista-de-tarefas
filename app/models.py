from django.db import models
from django.contrib.auth import get_user_model

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
    def __str__(self):
        return self.title