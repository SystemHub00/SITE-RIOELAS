from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid
import csv
from io import StringIO

# Armazena os leads inscritos em memória
leads = []

# Inicializa o Flask antes das rotas
app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'  # Troque por uma chave forte em produção

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        session['nome'] = request.form.get('nome')
        session['cpf'] = request.form.get('cpf')
        session['nascimento'] = request.form.get('nascimento')
        session['whatsapp'] = request.form.get('whatsapp')
        session['email'] = request.form.get('email')
        return redirect(url_for('endereco'))
    return render_template('inscricao.html')

@app.route('/endereco', methods=['GET', 'POST'])
def endereco():
    if request.method == 'POST':
        session['cep'] = request.form.get('cep')
        session['endereco'] = request.form.get('endereco')
        session['numero'] = request.form.get('numero')
        session['complemento'] = request.form.get('complemento')
        session['bairro'] = request.form.get('bairro')
        session['cidade'] = request.form.get('cidade')
        session['estado'] = request.form.get('estado')
        return redirect(url_for('curso'))
    return render_template('endereco.html')

@app.route('/curso', methods=['GET', 'POST'])
def curso():
    if request.method == 'POST':
        session['curso'] = request.form.get('curso')
        return redirect(url_for('revisao'))
    return render_template('curso.html')

@app.route('/revisao', methods=['GET', 'POST'])
def revisao():
    if request.method == 'POST':
        return redirect(url_for('confirmacao'))
    return render_template('revisao.html', dados=session)

@app.route('/confirmacao')
def confirmacao():
    # Gera protocolo único
    protocolo = str(uuid.uuid4())[:8]
    session['protocolo'] = protocolo
    # Monta os dados na ordem desejada
    dados = [
        protocolo,
        session.get('nome',''),
        session.get('cpf',''),
        session.get('nascimento',''),
        session.get('whatsapp',''),
        session.get('email',''),
        session.get('cep',''),
        session.get('endereco',''),
        session.get('numero',''),
        session.get('complemento',''),
        session.get('bairro',''),
        session.get('cidade',''),
        session.get('estado',''),
        session.get('curso','')
    ]
    # Salva os dados localmente para o dashboard admin
    leads.append(dados)
    return render_template('confirmacao.html', protocolo=protocolo)
# Rotas de admin (fora de qualquer função)
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if email == 'admfgm@gmail.com' and senha == '1234':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciais inválidas!')
    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    # Calcular quantidade de leads
    total_leads = len(leads)
    # Calcular média de idade
    from datetime import datetime
    idades = []
    for lead in leads:
        nascimento = lead[3]  # campo nascimento
        try:
            if nascimento:
                # Aceita formato DD/MM/AAAA
                dia, mes, ano = map(int, nascimento.split('/'))
                hoje = datetime.today()
                idade = hoje.year - ano - ((hoje.month, hoje.day) < (mes, dia))
                idades.append(idade)
        except Exception:
            pass
    media_idade = round(sum(idades) / len(idades), 1) if idades else 0
    return render_template('admin_dashboard.html', leads=leads, total_leads=total_leads, media_idade=media_idade)

@app.route('/download-csv')
def download_csv():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Protocolo','Nome','CPF','Nascimento','Whatsapp','Email','CEP','Endereço','Número','Complemento','Bairro','Cidade','Estado','Curso'])
    for lead in leads:
        writer.writerow(lead)
    output = si.getvalue()
    return app.response_class(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=leads.csv'}
    )

@app.route('/download-excel')
def download_excel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Protocolo','Nome','CPF','Nascimento','Whatsapp','Email','CEP','Endereço','Número','Complemento','Bairro','Cidade','Estado','Curso'])
    for lead in leads:
        writer.writerow(lead)
    output = si.getvalue()
    return app.response_class(
        output,
        mimetype='application/vnd.ms-excel',
        headers={'Content-Disposition': 'attachment;filename=leads.xls'}
    )

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
