from django import forms

from .models import Lista_tarefas

class TarefaForm(forms.ModelForm):
    class Meta: 
        model = Lista_tarefas
        fields = ['title', 'description']