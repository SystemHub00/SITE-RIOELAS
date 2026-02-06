from flask import Flask, render_template, request, redirect, url_for, session
import csv
import uuid

from gsheet_utils import append_to_sheet
import os
def ensure_gsheets_json():
    creds_env = os.environ.get('GOOGLE_SHEETS_CREDS_CONTENT')
    creds_path = os.environ.get('GOOGLE_SHEETS_CREDS', 'plated-field-474017-b8-e00d977b2612.json')
    if creds_env and not os.path.exists(creds_path):
        with open(creds_path, 'w', encoding='utf-8') as f:
            f.write(creds_env)
        print(f'Arquivo de credencial criado em: {creds_path}')
    else:
        print('Arquivo de credencial já existe ou variável de ambiente não definida.')

ensure_gsheets_json()
print('Arquivos no diretório atual:', os.listdir())
import traceback

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'  # Troque por uma chave forte em produção

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        from datetime import datetime
        nome = request.form.get('nome')
        if nome and len(nome) > 50:
            return render_template('inscricao.html', erro_nome='Nome deve ter no máximo 50 caracteres.')
        session['nome'] = nome
        session['cpf'] = request.form.get('cpf')
        nascimento = request.form.get('nascimento')
        session['nascimento'] = nascimento
        whatsapp = request.form.get('whatsapp')
        # Validação de DDD do WhatsApp
        ddds_validos = {
            '68','96','92','97','91','93','94','69','95','63', # Norte
            '82','71','73','74','75','77','85','88','98','99','83','81','87','86','89','84','79', # Nordeste
            '61','62','64','65','66','67', # Centro-Oeste
            '27','28','31','32','33','34','35','37','38','21','22','24','11','12','13','14','15','16','17','18','19', # Sudeste
            '41','42','43','44','45','46','47','48','49','51','53','54','55' # Sul
        }
        if whatsapp:
            import re
            match = re.match(r'^(\d{2})', whatsapp)
            if not match or match.group(1) not in ddds_validos:
                return render_template('inscricao.html', erro_whatsapp='DDD do WhatsApp inválido. Informe um número com DDD válido do Brasil.')
        session['whatsapp'] = whatsapp
        session['email'] = request.form.get('email')
        session['genero'] = request.form.get('genero')
        # Validação de idade máxima
        try:
            if nascimento:
                # Aceita tanto yyyy-mm-dd (formulário HTML) quanto dd/mm/yyyy (usuário)
                if '-' in nascimento:
                    data_nasc = datetime.strptime(nascimento, '%Y-%m-%d')
                else:
                    data_nasc = datetime.strptime(nascimento, '%d/%m/%Y')
                hoje = datetime.today()
                idade = (hoje - data_nasc).days // 365
                if idade > 90:
                    return render_template('inscricao.html', erro_nascimento='Idade permitida: de 18 até 90 anos')
                if idade < 18:
                    return render_template('inscricao.html', erro_nascimento='Idade permitida: de 18 até 90 anos')
        except Exception:
            return render_template('inscricao.html', erro_nascimento='Data de nascimento inválida.')
        return redirect(url_for('endereco'))
    return render_template('inscricao.html')

@app.route('/endereco', methods=['GET', 'POST'])
def endereco():
    if request.method == 'POST':
        cep = request.form.get('cep', '').replace('-', '').strip()
        if not (cep.isdigit() and len(cep) == 8):
            return render_template('endereco.html', erro_cep='CEP inválido. Informe no formato 00000-000.')
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
