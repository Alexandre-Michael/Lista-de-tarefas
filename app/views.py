from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TarefaForm
from .models import Lista_tarefas
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    search_query = request.GET.get('search', '')  # Obtém o termo de busca
    page_number = request.GET.get('page', 1)  # Obtém a página atual

    # Filtrar tarefas pelo título e ordenar por status e data de criação
    lista_tarefas = Lista_tarefas.objects.filter(
        Q(title__icontains=search_query, user=request.user)
    ).order_by('done', '-created_at') if search_query else Lista_tarefas.objects.filter(user=request.user).order_by('done', '-created_at')

    # Paginação das tarefas
    paginator = Paginator(lista_tarefas, 6)
    tarefas = paginator.get_page(page_number)

    no_results = not lista_tarefas.exists() if search_query else False

    if no_results:
        messages.info(request, "Nenhuma tarefa encontrada")

    print(tarefas)

    return render(request, 'home.html', {'tarefas': tarefas, 'search_query': search_query, 'no_results': no_results})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Validação de campos obrigatórios
            if not username or not password:
                messages.error(request, "Preencha todos os campos obrigatórios.")
                return redirect('login')
            
            # Verificação de autenticação
            user = authenticate(username = username, password = password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuário ou senha incorretos")
                return redirect('login')         
        else:
            return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        cadastro_username = request.POST.get('username')
        cadastro_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=cadastro_username).exists():
            messages.error(request, "Esse nome de usuário já está em uso.")
            return redirect('cadastro')
        
        if not cadastro_username or not cadastro_password:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('cadastro')
        
        if len(set(cadastro_password)) == 1:
            messages.error(request, "A senha não pode conter apenas caracteres repetidos.")
            return redirect('cadastro')
        
        if len(cadastro_password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return redirect('cadastro')
        
        # Verificação se as senhas coincidem
        if cadastro_password != confirm_password:
            messages.error(request, "As senhas estão diferentes.")
            return redirect('cadastro')
        
        user = User.objects.create_user(username = cadastro_username, password = cadastro_password)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect('login')
    else:
        return render(request, 'cadastro.html')

@login_required(login_url='login')
def tarefaview(request, id):
    tarefa = get_object_or_404(Lista_tarefas, pk=id)
    return render(request, 'tarefa.html', {'tarefa': tarefa})

@login_required(login_url='login')
def tarefanova(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        
        if not titulo:
            messages.error(request, "O campo de título deve ser preenchido")
            return render(request, 'tarefa-nova.html')
        
        tarefa = Lista_tarefas.objects.create(title=titulo, description=descricao, user = request.user)
        tarefa.save()
        return redirect('home')
    else:
        return render(request, 'tarefa-nova.html')

@login_required(login_url='login')
def editar_tarefa(request, id):
    # Obtém a tarefa existente ou retorna 404
    tarefa = get_object_or_404(Lista_tarefas, pk=id)
    
    if request.method == 'POST':
        titulo_edit = request.POST.get('titulo')  # Recupera o título do formulário
        descricao_edit = request.POST.get('descricao')  # Recupera a descrição do formulário
        status_edit = request.POST.get('status')
        
        if not titulo_edit:
            messages.error(request, "O campo de título deve ser preenchido")
            return render(request, 'editar-tarefa.html', {'tarefa': tarefa})
            

        # Atualiza os campos da tarefa
        tarefa.title = titulo_edit
        tarefa.description = descricao_edit 
        tarefa.done = status_edit
        tarefa.save()
        return redirect('home')# Redireciona para a página inicial

    # Renderiza o formulário pré-preenchido com os dados existentes
    return render(request, 'editar-tarefa.html', {'tarefa': tarefa})

@login_required(login_url='login')
def deletar_tarefa(request, id):
    tarefa = get_object_or_404(Lista_tarefas, pk=id)
    tarefa.delete()
    messages.success(request, "A tarefa foi deletada com sucesso")
    return redirect('home')

def error_404(request):
    return render(request, '404.html', status=404)

def helloworld(request):
    return HttpResponse("Hello World!")
