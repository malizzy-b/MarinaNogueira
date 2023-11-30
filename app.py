from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, template_folder='templates')

senhas_atendimento = []
senhas_comum = []
senhas_chamadas = []

proximas_senhas_atendimento = []
proximas_senhas_comum = []

@app.route('/')
def index():
    return render_template('index.html', senhas_atendimento=senhas_atendimento, senhas_comum=senhas_comum, senhas_chamadas=senhas_chamadas, proximas_senhas_atendimento=proximas_senhas_atendimento, proximas_senhas_comum=proximas_senhas_comum)

@app.route('/chamar_atendimento', methods=['POST'])
def chamar_atendimento():
    data = {}
    if proximas_senhas_atendimento:
        senha = proximas_senhas_atendimento.pop(0)
        senhas_chamadas.append(senha)
        senhas_atendimento.append(senha)
        data['senha_atendimento'] = senha
        data['senha_anterior'] = data['senha_anterior2'] = data['senha_anterior3'] = ''
        if senhas_chamadas:
            data['senha_anterior'] = senhas_chamadas[-1]
            if len(senhas_chamadas) > 1:
                data['senha_anterior2'] = senhas_chamadas[-2]
            if len(senhas_chamadas) > 2:
                data['senha_anterior3'] = senhas_chamadas[-3]

    return jsonify(data)

@app.route('/chamar_comum', methods=['POST'])
def chamar_comum():
    data = {}
    if proximas_senhas_comum:
        senha = proximas_senhas_comum.pop(0)
        senhas_chamadas.append(senha)
        senhas_comum.append(senha)
        data['senha_comum'] = senha
        data['senha_anterior'] = data['senha_anterior2'] = data['senha_anterior3'] = ''
        if senhas_chamadas:
            data['senha_anterior'] = senhas_chamadas[-1]
            if len(senhas_chamadas) > 1:
                data['senha_anterior2'] = senhas_chamadas[-2]
            if len(senhas_chamadas) > 2:
                data['senha_anterior3'] = senhas_chamadas[-3]

    return jsonify(data)

@app.route('/gerar_senha', methods=['POST'])
def gerar_senha():
    tipo = request.form['tipo_senha']
    if tipo == 'normal':
        nova_senha = 'B{:03d}'.format(len(proximas_senhas_comum) + 1)
        proximas_senhas_comum.append(nova_senha)
    elif tipo == 'preferencial':
        nova_senha = 'A{:03d}'.format(len(proximas_senhas_atendimento) + 1)
        proximas_senhas_atendimento.append(nova_senha)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
