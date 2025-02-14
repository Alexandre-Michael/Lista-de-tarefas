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
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('email-password-reset/', views.email_password_reset, name='email-password-reset'),
    path('token-password-reset/', views.token_password_reset, name='token-password-reset'),
    path('404/', views.error_404, name='404'),
    path('configuracoes/', views.configurações, name='configuracoes'),
    path('trocar-avatar/', views.trocar_avatar, name='trocar-avatar'),
    path('deletar-avatar/', views.deletar_avatar, name='deletar-avatar'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('reset-email/', views.reset_email, name='reset-email'),
    path('trocar-usuario/', views.trocar_usuario, name='trocar-usuario'),
]