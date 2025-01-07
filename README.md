# Projeto: Lista de Tarefas

Este projeto é uma aplicação web para gerenciar listas de tarefas. Ele foi desenvolvido utilizando o framework **Django** e é ideal para quem deseja organizar melhor suas atividades diárias. 

## Funcionalidades
- **Cadastro de Usuários**: Permite que novos usuários se registrem para criar suas próprias listas de tarefas.
- **Autenticação de Usuários**: Apenas usuários autenticados podem acessar suas tarefas.
- **Criação de Tarefas**: Adicione novas tarefas à lista com título e descrição.
- **Edição de Tarefas**: Atualize informações sobre suas tarefas existentes.
- **Exclusão de Tarefas**: Remova tarefas que não são mais necessárias.
- **Pesquisa de Tarefas**: Pesquise por tarefas específicas utilizando um campo de busca.
- **Sistema de Paginação**: Visualize as tarefas de forma organizada, com paginação para listas grandes.
- **Notificações**: Feedback visual para ações como sucesso ou erro (adicionar, excluir, etc.).

## Tecnologias Utilizadas
- **Linguagem**: Python
- **Framework**: Django
- **Banco de Dados**: SQLite (padrão do Django, mas pode ser alterado para outro)
- **HTML/CSS**: Com uso de **Bulma** para estilização
- **Outras Dependências**:
  - Django Messages (para notificações)
  - Django Authentication (para login e logout)

## Como Rodar o Projeto
### Pré-requisitos
- Python 3.10+
- Git (opcional, mas recomendado)
- Ambiente virtual configurado (venv)

### Passo a Passo
1. Clone o repositório (ou copie os arquivos):
   ```bash
   git clone <URL_DO_REPOSITORIO>
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
4. Configure o arquivo `.env`:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```env
   SECRET_KEY=sua-chave-secreta
   DEBUG=True or False (True para desenvolvimento, False para produção)
   ALLOWED_HOSTS=(example: ALLOWED_HOSTS=localhost,127.0.0.1,meudominio.com) Recomendado!! * para todos os hosts
   ```
5. Aplique as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
7. Acesse no navegador:
   - URL: `http://127.0.0.1:8000`

## Contribuindo
Sinta-se à vontade para contribuir com este projeto. Você pode:
- Abrir Issues com sugestões ou problemas encontrados.
- Criar Pull Requests para correções ou novas funcionalidades.

## Licença
Este projeto está licenciado sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
