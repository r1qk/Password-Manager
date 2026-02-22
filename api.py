from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import crud
import init_db

app = Flask(__name__)

#Configurando flask_jwt_extended (TOKENS)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app) #gera e verifica tokens


#Criar conta (POST -> usuário)
@app.route("/createAccount", methods=["POST"])
def create_account_api():
    dados = request.json #transforma a request do cliente em json pro servidor
    nome = dados.get("nome") 
    senha = dados.get("senha") 

    resultado = crud.create_account(nome, senha)

    if resultado.get("sucesso"):
        return jsonify(resultado), 201 #criado
    else:
        return jsonify(resultado), 409 #não criou porque já existe
    
#Login (POST -> usuário)
@app.route("/login", methods=["POST"])
def login_api():
    dados = request.json
    nome = dados.get("nome") 
    senha = dados.get("senha") 

    resultado = crud.login(nome, senha)
    
    if resultado.get("sucesso"):
        access_token = create_access_token(identity=nome) #token pra nome do usuário
        return jsonify({"status": "Logado com sucesso!" ,"Token de acesso": access_token}), 200 #ok
    else: 
        return jsonify({"Erro": "Nome ou senha inválidos"}), 401 #credenciais inválidas
    
#Criar senha (POST -> senha)
@app.route("/createPassword", methods=["POST"])
@jwt_required() #decorador para exigir o token
def create_password_api():
    nome = get_jwt_identity() #nome vem do token
    dados = request.json
    plataforma = dados.get("plataforma")
    senha = dados.get("senha")

    resultado = crud.create(nome, plataforma, senha)
    if resultado.get("sucesso"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 400 #Error
    
#Ler senhas (GET -> senha)
@app.route("/readPassword", methods=["GET"])
@jwt_required() 
def read_passwords_api():
    nome = get_jwt_identity()
    resultado = crud.read(nome)
    if resultado.get("sucesso"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 404
    
#Atualizar senha (PUT ou PATH -> senha)
@app.route("/updatePassword", methods=["PATCH"])
@jwt_required() 
def update_api():
    dados = request.json
    nome = get_jwt_identity()
    nova_senha = dados.get("nova_senha")
    plataforma = dados.get("plataforma")

    resultado = crud.update(nome, plataforma, nova_senha)    

    if resultado.get("sucesso"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 404 #nada encontrado (nenhum registro encontrado)
    
#Deletar senha
@app.route("/deletePassword", methods=["DELETE"])
@jwt_required() 
def delete_api():
    dados = request.json
    nome = get_jwt_identity()
    plataforma = dados.get("plataforma")

    resultado = crud.delete(nome, plataforma)
    if resultado.get("sucesso"):
        return jsonify(resultado), 200
    else: 
        return jsonify(resultado), 404 #nada deletado (nenhum registro encontrado)
    

if __name__ == "__main__":
    init_db.create_schema()
    init_db.create_table_usuary()
    init_db.create_table_password()
    app.run(debug=True)