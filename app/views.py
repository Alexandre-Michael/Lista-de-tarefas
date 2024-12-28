from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TarefaForm
from .models import Lista_tarefas
from django.contrib import messages
from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '')  # Obtém o termo de busca
    page_number = request.GET.get('page', 1)  # Obtém a página atual

    # Filtrar tarefas pelo título se a busca estiver presente
    lista_tarefas = Lista_tarefas.objects.filter(
        Q(title__icontains=search_query)
    ).order_by('-created_at') if search_query else Lista_tarefas.objects.all().order_by('-created_at')

    # Paginação das tarefas
    paginator = Paginator(lista_tarefas, 6)
    tarefas = paginator.get_page(page_number)

    no_results = not lista_tarefas.exists() if search_query else False

    if no_results:
        messages.info(request, "Nenhuma tarefa encontrada")

    print(tarefas)

    return render(request, 'home.html', {'tarefas': tarefas, 'search_query': search_query, 'no_results': no_results})

def tarefaview(request, id):
    tarefa = get_object_or_404(Lista_tarefas, pk=id)
    return render(request, 'tarefa.html', {'tarefa': tarefa})

def tarefanova(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        
        if not titulo:
            messages.error(request, "O campo de título deve ser preenchido")
            return render(request, 'tarefa-nova.html')
        
        tarefa = Lista_tarefas.objects.create(title=titulo, description=descricao) 
        tarefa.save()
        return redirect('home')
    else:
        return render(request, 'tarefa-nova.html')

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

def deletar_tarefa(request, id):
    tarefa = get_object_or_404(Lista_tarefas, pk=id)
    tarefa.delete()
    messages.success(request, "A tarefa foi deletada com sucesso")
    return redirect('home')

def helloworld(request):
    return HttpResponse("Hello World!")
