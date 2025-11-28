from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inscricao')
def inscricao():
    return render_template('inscricao.html')


@app.route('/endereco')
def endereco():
    return render_template('endereco.html')

@app.route('/curso')
def curso():
    return render_template('curso.html')

@app.route('/revisao')
def revisao():
    return render_template('revisao.html')

@app.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')

if __name__ == '__main__':
    app.run(debug=True)
