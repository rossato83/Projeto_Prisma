import os

from flask import Flask

app = Flask(__name__)  # Certifique-se de que esta linha está presente

@app.route("/")
def home():
    return "Site publicado com sucesso no Render! 🚀"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render define a porta automaticamente
    app.run(host="0.0.0.0", port=port, debug=False)

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///treinamentos.db"
db = SQLAlchemy(app)

# Modelo do banco de dados
class Treinamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    treinamento_id = db.Column(db.Integer, db.ForeignKey("treinamento.id"))
    status = db.Column(db.String(50), default="Pendente")  # Pendente ou Concluído

# Criar tabelas
with app.app_context():
    db.create_all()

# Página inicial
@app.route("/")
def index():
    treinamentos = Treinamento.query.all()
    funcionarios = Funcionario.query.all()
    return render_template("index.html", treinamentos=treinamentos, funcionarios=funcionarios)

# Adicionar treinamento
@app.route("/add_treinamento", methods=["POST"])
def add_treinamento():
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    novo_treinamento = Treinamento(nome=nome, descricao=descricao)
    db.session.add(novo_treinamento)
    db.session.commit()
    return redirect("/")

# Adicionar funcionário ao treinamento
@app.route("/add_funcionario", methods=["POST"])
def add_funcionario():
    nome = request.form["nome"]
    treinamento_id = request.form["treinamento_id"]
    novo_funcionario = Funcionario(nome=nome, treinamento_id=treinamento_id)
    db.session.add(novo_funcionario)
    db.session.commit()
    return redirect("/")

# Atualizar status do treinamento
@app.route("/update_status/<int:id>")
def update_status(id):
    funcionario = Funcionario.query.get(id)
    funcionario.status = "Concluído"
    db.session.commit()
    return redirect("/")

import pandas as pd
from flask import send_file

# Nova rota para exportar treinamentos e funcionários para Excel
@app.route("/export")
def export():
    # Buscar dados do banco
    treinamentos = Treinamento.query.all()
    funcionarios = Funcionario.query.all()

    # Criar DataFrames do Pandas
    df_treinamentos = pd.DataFrame([(t.id, t.nome, t.descricao) for t in treinamentos], columns=["ID", "Nome", "Descrição"])
    df_funcionarios = pd.DataFrame([(f.id, f.nome, f.treinamento_id, f.status) for f in funcionarios], columns=["ID", "Nome", "Treinamento ID", "Status"])

    # Criar um arquivo Excel com duas abas
    caminho_arquivo = "relatorio_treinamentos.xlsx"
    with pd.ExcelWriter(caminho_arquivo, engine="openpyxl") as writer:
        df_treinamentos.to_excel(writer, sheet_name="Treinamentos", index=False)
        df_funcionarios.to_excel(writer, sheet_name="Funcionários", index=False)

    # Enviar o arquivo para download
    return send_file(caminho_arquivo, as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug=True)
