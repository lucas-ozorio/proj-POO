from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessária para gerenciar a sessão

# Redireciona a raiz ('/') para a página de login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        senha = request.form.get('senha')

        # Validação simples: campos preenchidos
        if username and senha:
            if username == 'admin':  # Verifica se o nome de usuário é "admin"
                session['usuario'] = username  # Salva o nome do usuário na sessão
                flash('Bem-vindo, administrador!', 'success')
                return redirect(url_for('admin_page'))  # Redireciona para a página de admin
            else:
                session['usuario'] = username  # Salva o nome do usuário na sessão
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('home'))
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('favorites', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

# Rota para a página de administrador
@app.route('/admin_page')
def admin_page():
    if 'usuario' not in session or session['usuario'] != 'admin':
        flash('Acesso restrito! Faça login como administrador.', 'error')
        return redirect(url_for('login'))
    return render_template('admin.html')

# Rota para adicionar plano
@app.route('/add_plan')
def add_plan():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('adicionar_plano.html') 

# Rota para alterar plano
@app.route('/change_plan')
def change_plan():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('alterar_plano.html') 

# Rota para cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        username = request.form.get('usuario')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirmar-senha')

        # Validação simples: todos os campos preenchidos
        if nome and email and cpf and username and senha and confirma_senha:
            if senha == confirma_senha:
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('login'))
            else:
                flash('As senhas não coincidem.', 'error')
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    return render_template('signup.html')


# Rota para a página inicial
@app.route('/home')
def home():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar a página inicial.', 'error')
        return redirect(url_for('login'))
    return render_template('home.html', username=session['usuario'])

# Rota para a página de notícias
@app.route('/news')
def noticias():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('news.html')

# Rota para a página de ações
@app.route('/stocks')
def acoes():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('stocks.html')

# Rota para favoritos
@app.route('/favorites', methods=['GET', 'POST'])
def favoritos():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))

    if 'favorites' not in session:
        session['favorites'] = []

    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao:
            session['favorites'].append(acao)
            flash(f'Ação "{acao}" adicionada aos favoritos!', 'success')

    return render_template('favorites.html', favoritos=session['favorites'])

# Rota para assinatura
@app.route('/subscription', methods=['GET', 'POST'])
def cadastro_assinatura():
    if request.method == 'POST':
        tipoplano = request.form.get('tipo-plano')
        titularcartao = request.form.get('titular-cartao')
        numerocartao = request.form.get('numero-cartao')
        data_exp = request.form.get('data-expiracao')
        cpfcnpj = request.form.get('cpf-cnpj')
        cvc = request.form.get('cvc')
        banco = request.form.get('banco')

        # Validação simples: todos os campos preenchidos
        if tipoplano and titularcartao and numerocartao and data_exp and cpfcnpj and cvc and banco:
            flash('Assinatura realizada com sucesso!', 'success')
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    return render_template('subscription.html')

# Rota para clique em ações
@app.route('/stock_click')
def stock_click():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('stock_click.html')

# Rota para cobrança
@app.route('/billing')
def billing():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('billing.html')

# Rota para mensagens
@app.route('/message', methods=['GET', 'POST'])
def message():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        if mensagem:
            flash('Obrigado por nos enviar sua sugestão/mensagem.', 'success')
        else:
            flash('Por favor, escreva sua mensagem.', 'error')

    return render_template('message.html')

# Rota para ajuda
@app.route('/help', methods=['GET', 'POST'])
def help():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        ajuda = request.form.get('mensagem-ajuda')
        if ajuda:
            flash('Obrigado por nos enviar sua mensagem, responderemos em breve.', 'success')
        else:
            flash('Por favor, escreva sua mensagem.', 'error')

    return render_template('help.html')

@app.route('/edit_plan')
def edit_plan():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('editar_plano.html') 

@app.route('/editing_plan')
def editing_plan():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    return render_template('editando_plano.html') 

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)
