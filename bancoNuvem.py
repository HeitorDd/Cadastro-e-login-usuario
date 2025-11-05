import os
import re
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, session

load_dotenv()
app = Flask(__name__) 

app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "chave-padrao")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("Conectado ao Supabase com sucesso!")

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def cadastrar_usuario(email, senha):
    try:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(senha_bytes, salt)
        hash_senha_str = hash_senha.decode('utf-8')

        supabase.table('Cadastros').insert(
            {
                'email': email,
                'senha': hash_senha_str
            },
            returning="minimal"
        ).execute()
        
        return True

    except Exception as e:
        print(f"Erro no cadastro (Supabase): {e}")
        return f"Erro ao cadastrar: {e}"


def fazer_login(email, senha):
    try:
        response = supabase.table('Cadastros') \
                           .select('senha') \
                           .eq('email', email) \
                           .execute()

        if response.data:
            hash_salvo_str = response.data[0]['senha']
            hash_salvo_bytes = hash_salvo_str.encode('utf-8')
            senha_digitada_bytes = senha.encode('utf-8')

            if bcrypt.checkpw(senha_digitada_bytes, hash_salvo_bytes):
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        print(f"Erro inesperado no login: {e}")
        return False


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/registrar", methods=['POST'])
def handle_registrar():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not re.match(EMAIL_REGEX, email):
        flash("Formato de email inválido.", 'error')
        return redirect(url_for('index'))

    resultado = cadastrar_usuario(email, senha)
    
    if resultado is True:
        flash(f"Usuário '{email}' cadastrado com sucesso!", 'success')
    else:
        flash(f"Erro no cadastro. O email pode já existir.", 'error') 

    return redirect(url_for('index'))


@app.route("/login", methods=['POST'])
def handle_login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not re.match(EMAIL_REGEX, email):
        flash("Formato de email inválido.", 'error')
        return redirect(url_for('index'))

    if fazer_login(email, senha):
        flash(f"Login bem-sucedido! Bem-vindo, {email}.", 'success')
    else:
        flash("Email ou senha incorretos. Tente novamente.", 'error')
        
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)