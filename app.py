from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Variáveis para armazenar as senhas
senhas_atendimento = []
senhas_consulta = []
senhas_chamadas = []

@app.route('/')
def index():
    return render_template('index.html', senhas_atendimento=senhas_atendimento, senhas_consulta=senhas_consulta, senhas_chamadas=senhas_chamadas)

def chamar_atendimento():
    senha = request.form['senha_atendimento']
    senhas_chamadas.append(senha)
    return 'Chamada realizada com sucesso'

@app.route('/chamar_consulta', methods=['POST'])
def chamar_consulta():
    senha = request.form['senha_consulta']
    senhas_chamadas.append(senha)
    return 'Chamada realizada com sucesso'

@app.route('/gerar_senha', methods=['POST'])
def gerar_senha():
    tipo = request.form['tipo_senha']
    if tipo == 'normal':
        nova_senha = 'B{:03d}'.format(len(senhas_atendimento) + 1)
        senhas_atendimento.append(nova_senha)
    elif tipo == 'preferencial':
        nova_senha = 'A{:03d}'.format(len(senhas_consulta) + 1)
        senhas_consulta.append(nova_senha)

    # Adiciona a senha gerada à lista
   

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)