from django.db import models

class Lista_tarefas(models.Model):

    STATUS = (
        ('Fazendo', 'fazendo'),
        ('Feito', 'feito'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    done = models.CharField(max_length=7, choices=STATUS, default='Fazendo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title