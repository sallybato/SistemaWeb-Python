# SistemaWeb-Python
TRABALHO FINAL  (Sistema Web com Login e Área Restrita (Flask + SQLite)) 
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação do Projeto TaskFlow</title>
    <!-- Link para Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Estilos Adicionais -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #e9ecef; /* Fundo cinza claro */
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .readme-container {
            background-color: #ffffff;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        }
        h1, h2, h3 {
            border-bottom: 2px solid #007bff; /* Cor primária do Bootstrap */
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
            color: #007bff;
        }
        /* Estilo para blocos de código */
        pre {
            background-color: #f8f9fa;
            border: 1px solid #ced4da;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
        }
        table {
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="readme-container">
            <h1 class="text-primary border-bottom border-primary pb-3 mb-4">
                <span style="font-size: 1.5rem;">📌</span> TaskFlow: Sistema de Gerenciamento de Tarefas Pessoais
            </h1>

            <p class="lead">
                O TaskFlow é uma aplicação web simples desenvolvida em Python (Flask) para gerenciar tarefas e compromissos pessoais, com foco na autenticação e controle de acesso individualizado. Cada usuário possui sua própria área restrita (Dashboard) para criar, listar e excluir suas suas tarefas.
            </p>

            <h2 class="mt-5 border-primary">
                <span style="font-size: 1.2rem;">✨</span> Funcionalidades Principais
            </h2>
            <ul class="list-group list-group-flush mb-4">
                <li class="list-group-item"><strong>Cadastro de Usuários:</strong> Criação de novas contas com verificação de e-mail único.</li>
                <li class="list-group-item"><strong>Autenticação Segura (Login/Logout):</strong> Uso de sessões Flask para manter o estado de login.</li>
                <li class="list-group-item"><strong>Criptografia de Senha:</strong> Todas as senhas são armazenadas como hash seguro utilizando `werkzeug.security`.</li>
                <li class="list-group-item"><strong>Dashboard Restrito:</strong> Acesso exclusivo após o login, exibindo apenas as tarefas do usuário logado.</li>
                <li class="list-group-item"><strong>CRUD de Tarefas:</strong> Capacidade de Cadastrar (Create), Listar (Read) e Excluir (Delete) tarefas pessoais.</li>
                <li class="list-group-item"><strong>Design Responsivo:</strong> Utilização do Bootstrap 5 para uma interface moderna e adaptável a diferentes dispositivos.</li>
            </ul>

            <h2 class="mt-5 border-primary">
                <span style="font-size: 1.2rem;">🛠️</span> Tecnologias Utilizadas
            </h2>
            <table class="table table-bordered table-striped">
                <thead class="table-primary">
                    <tr>
                        <th>Categoria</th>
                        <th>Tecnologia</th>
                        <th>Uso no Projeto</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Backend</strong></td><td>Python 3.x</td><td>Linguagem principal de desenvolvimento.</td></tr>
                    <tr><td><strong>Framework Web</strong></td><td>Flask</td><td>Servidor web leve e micro-framework.</td></tr>
                    <tr><td><strong>Banco de Dados</strong></td><td>SQLite3</td><td>Banco de dados leve e embutido (`banco.db`).</td></tr>
                    <tr><td><strong>Segurança</strong></td><td>`werkzeug.security`</td><td>Geração e verificação de hash de senhas.</td></tr>
                    <tr><td><strong>Frontend/Design</strong></td><td>Bootstrap 5</td><td>Framework CSS para o design e responsividade.</td></tr>
                    <tr><td><strong>Templates</strong></td><td>Jinja2</td><td>Motor de templates padrão do Flask.</td></tr>
                </tbody>
            </table>

            <h2 class="mt-5 border-primary">
                <span style="font-size: 1.2rem;">📁</span> Estrutura do Projeto
            </h2>
            <p>A estrutura de pastas segue as convenções do Flask para organização de código, templates e arquivos estáticos.</p>
            <pre><code>projeto/
│
├── app.py              # Lógica principal, rotas, e manipulação do DB
├── banco.db            # Arquivo do banco de dados SQLite (criado automaticamente)
├── templates/          # Arquivos HTML (Jinja2)
│  ├── base.html       # Layout principal com Bootstrap e nav
│  ├── index.html      # Página inicial
│  ├── login.html      # Formulário de login
│  ├── cadastro.html   # Formulário de cadastro
│  └── dashboard.html  # Área restrita (CRUD de tarefas)
└── static/
  └── style.css       # Estilos CSS personalizados (complemento do Bootstrap)
</code></pre>

            <h2 class="mt-5 border-primary">
                <span style="font-size: 1.2rem;">⚙️</span> Instalação e Execução
            </h2>
            <p>Siga os passos abaixo para configurar e rodar a aplicação localmente.</p>

            <h3 class="mt-4 text-secondary border-secondary">Pré-requisitos</h3>
            <p>Certifique-se de ter o <strong>Python 3.x</strong> instalado em seu sistema.</p>

            <h3 class="mt-4 text-secondary border-secondary">1. Criar e Ativar Ambiente Virtual (Recomendado)</h3>
            <pre><code># Cria o ambiente virtual
python -m venv venv

# Ativação (Windows)
.\venv\Scripts\activate

# Ativação (macOS/Linux)
source venv/bin/activate
</code></pre>

            <h3 class="mt-4 text-secondary border-secondary">2. Instalar Dependências</h3>
            <p>Com o ambiente virtual ativado, instale as bibliotecas Flask e Werkzeug.</p>
            <pre><code>pip install Flask werkzeug</code></pre>

            <h3 class="mt-4 text-secondary border-secondary">3. Executar a Aplicação</h3>
            <p>A aplicação cria o arquivo `banco.db` e as tabelas necessárias automaticamente na primeira execução.</p>
            <pre><code>python app.py</code></pre>

            <h3 class="mt-4 text-secondary border-secondary">4. Acesso</h3>
            <p>Após executar, acesse a URL no seu navegador:</p>
            <pre><code>http://127.0.0.1:5000/</code></pre>

            <h2 class="mt-5 border-primary">
                <span style="font-size: 1.2rem;">🔒</span> Modelo de Banco de Dados
            </h2>
            <p>O projeto utiliza duas tabelas relacionadas no SQLite3:</p>

            <h3 class="mt-4 text-secondary border-secondary">`usuario`</h3>
            <p>Responsável pelo armazenamento dos dados de autenticação.</p>
            <table class="table table-bordered table-striped">
                <thead class="table-info">
                    <tr><th>Coluna</th><th>Tipo</th><th>Restrições</th><th>Descrição</th></tr>
                </thead>
                <tbody>
                    <tr><td>`id`</td><td>INTEGER</td><td>PRIMARY KEY, AUTOINCREMENT</td><td>Identificador único do usuário.</td></tr>
                    <tr><td>`nome`</td><td>TEXT</td><td>NOT NULL</td><td>Nome completo do usuário.</td></tr>
                    <tr><td>`email`</td><td>TEXT</td><td>UNIQUE, NOT NULL</td><td>E-mail usado para login (único).</td></tr>
                    <tr><td>`senha`</td><td>TEXT</td><td>NOT NULL</td><td>Hash da senha criptografada.</td></tr>
                </tbody>
            </table>

            <h3 class="mt-4 text-secondary border-secondary">`tarefa`</h3>
            <p>Armazena os itens de tarefa, ligados ao usuário.</p>
            <table class="table table-bordered table-striped">
                <thead class="table-info">
                    <tr><th>Coluna</th><th>Tipo</th><th>Restrições</th><th>Descrição</th>