# Projeto: Lista de Tarefas

Este projeto é uma aplicação web para gerenciar listas de tarefas. Ele foi desenvolvido utilizando o framework **Django** e é ideal para quem deseja organizar melhor suas atividades diárias.

## Funcionalidades
- **CRUD de Tarefas**: Permite **Criar, Ler, Atualizar e Deletar** tarefas na lista de forma simples e intuitiva.
- **Cadastro de Usuários**: Usuários podem se registrar para acessar suas próprias listas de tarefas.
- **Autenticação de Usuários**: Apenas usuários autenticados podem acessar suas tarefas.
- **Pesquisa de Tarefas**: Pesquise por tarefas específicas utilizando um campo de busca.
- **Sistema de Paginação**: Visualize as tarefas de forma organizada, com paginação para listas grandes.
- **Notificações**: Feedback visual para ações como sucesso ou erro (adicionar, excluir, etc.).
- **Gerenciamento de Senhas e Reset via Email:** Usuários podem redefinir suas senhas através de link enviado por email, utilizando tokens para segurança.

## Tecnologias Utilizadas
- **Linguagem**: Python
- **Framework**: Django
- **Banco de Dados**: SQLite (padrão do Django, mas pode ser alterado para outro)
- **HTML/CSS**: Com uso de **Bulma** para estilização

## Como Rodar o Projeto
### Pré-requisitos
- Python 3.10+
- Git (opcional, mas recomendado)
- Ambiente virtual configurado (venv)

### Passo a Passo
1. Clone o repositório (ou copie os arquivos):
   ```bash
   git clone https://github.com/Alexandre-Michael/Lista-de-tarefas.git
   cd nome-do-projeto
   ```
2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   # Ative o ambiente virtual
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o arquivo `.env`**:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (você pode encontrar no .env.exemple):
   ```ini
   SECRET_KEY=sua-chave-secreta
   DEBUG=True  # Defina como False em produção
   ALLOWED_HOSTS=localhost,127.0.0.1,meudominio.com  # Adicione os domínios permitidos
   
   # Configuração de Email (para recuperação de senha, por exemplo)
   EMAIL_HOST=smtp.seuprovedor.com
   EMAIL_PORT=587 
   EMAIL_HOST_USER=seu-email@exemplo.com
   EMAIL_HOST_PASSWORD=sua-senha
   EMAIL_USE_TLS=True
   
   ```
5. Aplique as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Crie um superusuário (opcional, mas recomendado):
   ```bash
   python manage.py createsuperuser
   ```
7. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
8. Acesse no navegador:
   - URL: `http://127.0.0.1:8000`

## Contribuindo
Sinta-se à vontade para contribuir com este projeto. Você pode:
- Abrir Issues com sugestões ou problemas encontrados.
- Criar Pull Requests para correções ou novas funcionalidades.

## Licença
Este projeto está licenciado sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
