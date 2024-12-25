from django import forms

from .models import Lista_tarefa

class TarefaForm(forms.ModelForm):
    class Meta: 
        model = Lista_tarefa
        fields = ['title', 'description']