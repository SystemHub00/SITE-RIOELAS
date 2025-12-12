from flask import Flask, render_template, request, redirect, url_for, session
import csv
import uuid

from gsheet_utils import append_to_sheet
import os
import traceback

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
        session['como_conheceu'] = request.form.get('como_conheceu')
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
        session.get('curso',''),
        session.get('como_conheceu','')
    ]
    try:
        append_to_sheet(dados)
    except Exception as e:
        print('Erro ao salvar na planilha:', e)
        traceback.print_exc()
    return render_template('confirmacao.html', protocolo=protocolo)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
