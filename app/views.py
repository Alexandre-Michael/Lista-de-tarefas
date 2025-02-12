from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Lista_tarefas, password_reset_token, CustomUser
from uuid import uuid4
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from dotenv import load_dotenv
import os


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
        cadastro_email = request.POST.get('email')

        # Verificação de usuário já existente
        if CustomUser.objects.filter(username=cadastro_username).exists():
            messages.error(request, "Esse nome de usuário já está em uso.")
            return redirect('cadastro')
        
        # Verifica se o email já está em uso
        if CustomUser.objects.filter(email=cadastro_email).exists():
            messages.error(request, "Esse email já está cadastrado.")
            return redirect('cadastro')

        # Validação de campos obrigatórios
        if not cadastro_username or not cadastro_password or not cadastro_email:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('cadastro')
        
        # Verificação se a senha contém apenas caracteres repetidos
        if len(set(cadastro_password)) == 1:
            messages.error(request, "A senha não pode conter apenas caracteres repetidos.")
            return redirect('cadastro')
        
        # Verificação se a senha tem pelo menos 6 caracteres
        if len(cadastro_password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return redirect('cadastro')
        
        # Verificação se as senhas coincidem
        if cadastro_password != confirm_password:
            messages.error(request, "As senhas estão diferentes.")
            return redirect('cadastro')
        
        # Criação do usuário
        user = CustomUser.objects.create_user(username = cadastro_username, password = cadastro_password, email = cadastro_email)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect('login')
    else:
        return render(request, 'cadastro.html')

def email_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Validação de campos obrigatórios
        if not username or not email:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('email-password-reset')

        # Verificação se o email corresponde ao usuário informado
        user = CustomUser.objects.filter(username=username, email=email).first()
        if not user:
            messages.error(request, "O email não corresponde ao usuário informado.")
            return redirect('email-password-reset')

        # Verificação de email existente
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Esse email não está cadastrado.")
            return redirect('email-password-reset')

        # Criação do token
        # Usando uuid para gerar um token único
        token = uuid4().hex

        # Armazenando o token no banco de dados
        token_entry = password_reset_token.objects.create(user=user, token=token)  # Passando a instância do usuário
        token_entry.save()

        # Determina a URL base com base no ambiente
        if os.getenv('DEBUG') == 'True':
            reset_base_url = os.getenv('DEV_RESET_PASSWORD_URL')
        else:
            reset_base_url = os.getenv('PROD_RESET_PASSWORD_URL')

        reset_link = f"{reset_base_url}/token-password-reset/?token={token}"
        # Envia o link de recuperação de senha por email
        send_mail(
            subject='Redefinição de Senha',
            message= f'Use este link para redefinir sua senha.\n{reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        
        # Mensagem de sucesso de envio do email e redirecionamento
        messages.success(request, "Email de recuperação de senha enviado com sucesso. Confira sua caixa de entrada.")
        return redirect('login')
    return render(request, 'email-password-reset.html')

def token_password_reset(request):
    # Recupera o token da URL
    token = request.GET.get('token')

    # Validação do token
    token_entry = password_reset_token.objects.filter(token=token).first()
    if not token_entry or not token_entry.is_valid():
        messages.error(request, "Token inválido ou expirado.")
        return redirect('login')
        
    # Verifica se o token já foi usado
    if token_entry.is_used:
        messages.error(request, "Token já utilizado.")
        return redirect('login')
    
    # Formulário de redefinição de senha
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validação das novas senhas
        if not new_password or not confirm_password:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect(reverse('token-password-reset') + f"?token={token}")  # Usar reverse para construir a URL com token
        
        # Verificação se as senhas coincidem
        if new_password != confirm_password:
            messages.error(request, "As senhas estão diferentes.")
            return redirect(reverse('token-password-reset') + f"?token={token}")  # Usar reverse para construir a URL com token
        
        # Verificação se a senha contém apenas caracteres repetidos
        if len(set(new_password)) == 1:
            messages.error(request, "A senha não pode conter apenas caracteres repetidos.")
            return redirect(reverse('token-password-reset') + f"?token={token}")  # Usar reverse para construir a URL com token

        # Verificação se a nova senha é igual à anterior
        if token_entry.user.check_password(new_password):
            messages.error(request, "A nova senha não pode ser igual à anterior.")
            return redirect(reverse('token-password-reset') + f"?token={token}")   # Usar reverse para construir a URL com token

        # Atualizar a senha do usuário
        user = token_entry.user
        user.set_password(confirm_password)
        user.save()

        # Excluir o token para evitar reutilização
        token_entry.delete()

        messages.success(request, "Senha redefinida com sucesso. Faça login com sua nova senha.")
        return redirect('login')

    # GET: Renderizar a página de redefinição com o token
    token = request.GET.get('token')
    return render(request, 'token-password-reset.html')
    

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

@login_required(login_url='login')
def configurações(request):
    return render(request, 'configuracoes.html')

@login_required(login_url='login')
def trocar_avatar(request):
    if request.method == 'POST':
        user = request.user
        if 'resume' in request.FILES:
            avatar = request.FILES['resume']
            user.profile_picture = avatar
            print("A: ",user.profile_picture)
        user.save()
        print("B: ",user.profile_picture)
        messages.success(request, "Imagem de perfil atualizada com sucesso")
    return redirect('configuracoes')

@login_required(login_url='login')
def deletar_avatar(request):
    if request.method == 'POST':
        user = request.user
        if user.profile_picture:  # Verifica se o usuário tem um avatar definido
            avatar_path = user.profile_picture.path  # Obtém o caminho absoluto do arquivo
            if os.path.exists(avatar_path):  # Verifica se o arquivo realmente existe
                os.remove(avatar_path)  # Remove o arquivo do sistema de arquivos
                user.profile_picture = None  # Define o avatar como None no banco de dados
                user.save()
                messages.success(request, "Imagem de perfil deletada com sucesso")
            else:
                messages.error(request, "O arquivo do avatar não foi encontrado")
        else:
            messages.error(request, "Você não possui um avatar definido")
    return redirect('configuracoes')

@login_required(login_url='login')
def reset_email(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Preencha o campo obrigatório.")
            return redirect('configuracoes')
        if user.email == email:
            messages.error(request, "O email informado é igual ao atual.")
            return redirect('configuracoes')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "O email informado já está cadastrado.")
            return redirect('configuracoes')
        else:    
            user.email = email
            user.save()
            messages.success(request, "Email redefinido com sucesso")
    return redirect('configuracoes')

@login_required(login_url='login')
def reset_password(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not user.check_password(password):
            messages.error(request, "Senha atual incorreta.")
            return redirect('configuracoes')
        if not new_password or not confirm_password:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('configuracoes')
        if new_password != confirm_password:
            messages.error(request, "As senhas estão diferentes.")
            return redirect('configuracoes')
        if len(set(new_password)) == 1:
            messages.error(request, "A senha não pode conter apenas caracteres repetidos.")
            return redirect('configuracoes')
        user.set_password(confirm_password)
        user.save()
        auth_login(request, user) # Mantém o usuário logado após a troca de senha
        messages.success(request, "Senha redefinida com sucesso")
    return redirect('configuracoes')

def error_404(request):
    return render(request, '404.html', status=404)

def helloworld(request):
    return HttpResponse("Hello World!")
