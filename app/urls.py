from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tarefa/<int:id>', views.tarefaview, name='tarefa'),
    path('tarefanova/', views.tarefanova, name='tarefa-nova'),
    path('editar-tarefa/<int:id>', views.editar_tarefa, name='editar-tarefa'),
    path('deletar-tarefa/<int:id>', views.deletar_tarefa, name='deletar-tarefa'),
    path('helloworld/', views.helloworld),
]
