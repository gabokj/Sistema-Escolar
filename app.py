from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'  # Use uma chave forte e segura na produção!

alunos = []
USUARIO = 'adm'
SENHA = '1234'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == USUARIO and senha == SENHA:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Decorador para proteger rotas
def login_requerido(f):
    from functools import wraps
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

# Proteger rotas com login
@app.route('/')
@login_requerido
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['GET', 'POST'])
@login_requerido
def calcular():
    media = None
    situacao = ""
    if request.method == 'POST':
        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])
        media = (nota1 + nota2 + nota3) / 3
        situacao = "Aprovado" if media >= 7 else "Reprovado"
    return render_template('calcular.html', media=media, situacao=situacao)

@app.route('/cadastro', methods=['GET', 'POST'])
@login_requerido
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        classe = request.form['classe']
        media = float(request.form['media'])
        situacao = "Aprovado" if media >= 7 else "Reprovado"
        alunos.append({
            'nome': nome,
            'classe': classe,
            'media': media,
            'situacao': situacao
        })
        return redirect(url_for('lista'))
    return render_template('cadastro.html')

@app.route('/lista')
@login_requerido
def lista():
    return render_template('lista.html', alunos=alunos)

@app.route('/deletar/<int:index>', methods=['POST'])
@login_requerido
def deletar(index):
    if 0 <= index < len(alunos):
        alunos.pop(index)
    return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True)

