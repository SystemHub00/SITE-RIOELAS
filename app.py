from flask import Flask, render_template, request, redirect, url_for, session
import csv
import uuid

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configurações de e-mail via variáveis de ambiente
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
E_MAIL = os.getenv('E_MAIL', 'confemail75@gmail.com')
EMAIL_USER = os.getenv('EMAIL_USER', E_MAIL)    
EMAIL_PASS = 'sqie ybvj zgak kljq'
EMAIL_TO = 'confemail75@gmail.com'
IMAP_USER = os.getenv('IMAP_USER', 'confemail75@gmail.com')

def enviar_email_inscricao(dados):
    assunto = 'Nova inscrição recebida - Rio+Elas'
    corpo = 'Nova inscrição recebida:\n\n'
    campos = [
        'Protocolo', 'Nome', 'Gênero', 'CPF', 'Nascimento', 'Whatsapp', 'Email',
        'CEP', 'Endereço', 'Número', 'Complemento', 'Bairro', 'Cidade', 'Estado',
        'Local', 'Curso', 'Turma'
    ]
    # Montar lista de dados na mesma ordem dos campos
    dados_completos = [
        dados[0], # Protocolo
        dados[1], # Nome
        session.get('genero',''),
        dados[2], # CPF
        dados[3], # Nascimento
        dados[4], # Whatsapp
        dados[5], # Email
        dados[6], # CEP
        dados[7], # Endereço
        dados[8], # Número
        dados[9], # Complemento
        dados[10], # Bairro
        dados[11], # Cidade
        dados[12], # Estado
        session.get('local',''),
        session.get('curso',''),
        session.get('turma','')
    ]
    for campo, valor in zip(campos, dados_completos):
        corpo += f'{campo}: {valor}\n'
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
    except Exception as e:
        print('Erro ao enviar e-mail:', e)

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
        session['genero'] = request.form.get('genero')
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
        session['local'] = request.form.get('local')
        session['curso'] = request.form.get('curso')
        session['turma'] = request.form.get('turma')
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
    # Salva os dados localmente em DADOS.csv
    try:
        with open('dados/DADOS.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(dados)
    except Exception as e:
        print('Erro ao salvar em DADOS.csv:', e)
    try:
        enviar_email_inscricao(dados)
    except Exception as e:
        print('Erro ao enviar e-mail:', e)
    return render_template('confirmacao.html', protocolo=protocolo)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
