from django.contrib import admin
from .models import Lista_tarefas

admin.site.register(Lista_tarefas)

class Lista_tarefasAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'done', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'done', 'created_at', 'updated_at')