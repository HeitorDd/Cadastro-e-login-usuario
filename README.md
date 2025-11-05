Sistema de Login com Flask e Supabase
Este é um projeto de exemplo que demonstra a criação de um sistema de autenticação de usuários (login e cadastro) utilizando Python com o micro-framework Flask no backend e o Supabase como banco de dados.
As senhas são armazenadas de forma segura, passando por um processo de hashing com a biblioteca bcrypt antes de serem salvas no banco de dados.
✨ Funcionalidades
Cadastro de Usuários: Permite que novos usuários criem uma conta.
Login de Usuários: Autentica usuários existentes.
Hashing de Senha: Utiliza bcrypt para garantir que as senhas nunca sejam armazenadas em texto plano.
Interface Simples: Uma página única (HTML/CSS) com formulários para login e cadastro.
Notificações: Exibe mensagens de sucesso ou erro (flash messages) para o usuário.
Gerenciamento de Chaves: Utiliza um arquivo .env para proteger as chaves de API e a chave secreta da aplicação.
🔧 Tecnologias Utilizadas
Backend: Python 3
Framework Web: Flask
Banco de Dados: Supabase (PostgreSQL)
Cliente Python (DB): supabase-py
Segurança: bcrypt
Variáveis de Ambiente: python-dotenv
Frontend: HTML e CSS
⚙️ Como Funciona
O projeto é centralizado no arquivo app.py, que atua como o servidor backend.
Interface (Frontend): O arquivo templates/index.html renderiza os dois formulários (Login e Cadastro). Ele usa {{ url_for('static', ...) }} para carregar o CSS e exibe mensagens de flash enviadas pelo Flask.
Servidor (Backend): O app.py (Flask) define três rotas principais:
@app.route("/"): Carrega a página index.html.
@app.route("/registrar", methods=['POST']): Recebe os dados do formulário de cadastro. Ele chama a função cadastrar_usuario(), que gera o hash da senha com bcrypt e, em seguida, insere o email e o hash_da_senha na tabela Cadastros do Supabase.
@app.route("/login", methods=['POST']): Recebe os dados do formulário de login. Ele chama a função fazer_login(), que:
Busca no Supabase se existe um usuário com o email fornecido.
Se o usuário existe, ele obtém o hash da senha armazenado no banco.
Ele usa bcrypt.checkpw() para comparar a senha que o usuário digitou com o hash armazenado.
Se a comparação for verdadeira, o login é bem-sucedido.
Banco de Dados (Supabase): Uma única tabela (Cadastros) é usada para armazenar as colunas email e senha (que, na verdade, contém o hash da senha).
🚀 Como Rodar o Projeto Localmente
Siga estes passos para configurar e executar o projeto em sua máquina.
1. Pré-requisitos
Python 3.10 ou superior.
Conta no Supabase: Você precisará de um projeto Supabase para obter a URL e a chave da API.
2. Configuração do Banco de Dados (Supabase)
Faça login no Supabase e crie um novo projeto.
No menu lateral, vá para Table Editor e clique em "Create a new table".
Nomeie a tabela como Cadastros (exatamente como no código).
Adicione as seguintes colunas:
email (tipo text ou varchar). Importante: Marque a opção "Is Unique" para evitar e-mails duplicados.
senha (tipo text ou varchar).
Desative o Row Level Security (RLS) para esta tabela (ou crie as políticas de acesso adequadas) para permitir que o script Python insira e leia os dados.
3. Configuração do Ambiente Local
Baixe o projeto:
Nesta página do GitHub, clique no botão verde "<> Code".
Selecione "Download ZIP".
Extraia o arquivo .zip em uma pasta no seu computador.
Abra o terminal/prompt de comando dentro dessa pasta extraída (ela deve conter o arquivo app.py).
Crie e ative um ambiente virtual:
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate


Instale as dependências:
pip install -r requirements.txt


4. Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto (na mesma pasta do app.py).
Obtenha as chaves do Supabase:
No seu projeto Supabase, vá em Project Settings > API.
Copie o valor de Project URL.
Copie o valor da chave service_role (em "Project API keys").
Gere uma Chave Secreta do Flask:
No seu terminal, rode o comando abaixo para gerar uma chave segura:
python -c "import secrets; print(secrets.token_hex(32))"


Copie a chave gerada.
Adicione tudo ao arquivo .env:
# Cole a URL do seu projeto Supabase
SUPABASE_URL=https://[seu-projeto-url].supabase.co

# Cole sua chave 'service_role' (NÃO a 'anon public')
SUPABASE_KEY=[sua-chave-service-role-aqui]

# Cole a chave que você gerou no passo anterior
FLASK_SECRET_KEY=[sua-chave-secreta-do-flask-aqui]


5. Executando a Aplicação
Com o ambiente virtual ativado e o arquivo .env configurado, inicie o servidor Flask:
python app.py


O servidor estará rodando. Abra seu navegador e acesse:
http://127.0.0.1:5000
