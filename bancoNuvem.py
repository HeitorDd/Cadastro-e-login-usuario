import os
import re
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, session

# --- Configuração Inicial ---
load_dotenv()
app = Flask(__name__) # Inicializa o aplicativo Flask

# Chave secreta para 'flash messages' e 'session'
# Em produção, use um valor longo e aleatório
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "chave-padrao")

# --- Conexão com Supabase (Igual ao seu original) ---
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("Conectado ao Supabase com sucesso!")

# Regex (Igual ao seu original)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


# --- LÓGICA DE NEGÓCIO (Modificada para retornar True/False em vez de imprimir) ---

def cadastrar_usuario(email, senha):
    """
    (v3 Web) Faz o hash e insere o usuário.
    Retorna True em sucesso, ou uma string de erro em falha.
    """
    try:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(senha_bytes, salt)
        hash_senha_str = hash_senha.decode('utf-8')

        # Insere no banco
        supabase.table('Cadastros').insert(
            {
                'email': email,
                'senha': hash_senha_str
            },
            returning="minimal"
        ).execute()
        
        return True # Sucesso

    except Exception as e:
        # Pega erros (ex: email duplicado)
        print(f"Erro no cadastro (Supabase): {e}")
        return f"Erro ao cadastrar: {e}"


def fazer_login(email, senha):
    """
    (v3 Web) Verifica o email e a senha.
    Retorna True em sucesso, False em falha.
    """
    try:
        # 1. Busca o usuário APENAS pelo email
        response = supabase.table('Cadastros') \
                           .select('senha') \
                           .eq('email', email) \
                           .execute()

        # 2. Verifica se a lista 'response.data' tem algum resultado
        if response.data:
            hash_salvo_str = response.data[0]['senha']
            hash_salvo_bytes = hash_salvo_str.encode('utf-8')
            senha_digitada_bytes = senha.encode('utf-8')

            # 3. Compara a senha digitada com o hash salvo
            if bcrypt.checkpw(senha_digitada_bytes, hash_salvo_bytes):
                return True # Login bem-sucedido
            else:
                return False # Senha incorreta
        else:
            return False # Email não encontrado

    except Exception as e:
        print(f"Erro inesperado no login: {e}")
        return False


# --- ROTAS DO SITE (A "Tela") ---

@app.route("/")
def index():
    """ Rota principal, carrega a página HTML. """
    return render_template('index.html')


@app.route("/registrar", methods=['POST'])
def handle_registrar():
    """ Rota que recebe os dados do formulário de cadastro. """
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not re.match(EMAIL_REGEX, email):
        flash("Formato de email inválido.", 'error')
        return redirect(url_for('index'))

    resultado = cadastrar_usuario(email, senha)
    
    if resultado is True:
        flash(f"Usuário '{email}' cadastrado com sucesso!", 'success')
    else:
        # Mostra o erro que a função retornou
        flash(f"Erro no cadastro. O email pode já existir.", 'error') 

    return redirect(url_for('index')) # Volta para a página inicial


@app.route("/login", methods=['POST'])
def handle_login():
    """ Rota que recebe os dados do formulário de login. """
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not re.match(EMAIL_REGEX, email):
        flash("Formato de email inválido.", 'error')
        return redirect(url_for('index'))

    if fazer_login(email, senha):
        # 'flash' é uma mensagem temporária mostrada na tela
        flash(f"Login bem-sucedido! Bem-vindo, {email}.", 'success')
    else:
        flash("Email ou senha incorretos. Tente novamente.", 'error')
        
    return redirect(url_for('index')) # Volta para a página inicial


# --- Executa o servidor web ---
if __name__ == "__main__":
    # debug=True reinicia o servidor automaticamente quando você salva o .py
    app.run(debug=True, port=5000)