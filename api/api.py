from flask import Flask, jsonify, request
import db.crud as crud
import db.init_db as init_db
import encryption.rsa as rsa

app = Flask(__name__)


#Criar conta (POST -> usuário)
@app.route("/createAccount", methods=["POST"])
def create_account_api():
    dados = request.json #transforma a request do cliente em json pro servidor
    payload = rsa.rsa_decode_API(dados)

    nome = payload.get("nome") 
    senha = payload.get("senha") 
    salt = payload.get("salt")

    resultado = crud.create_account(nome, senha, salt)

    if resultado.get("status"):
        return jsonify(resultado), 201 #criado
    else:
        return jsonify(resultado), 409 #não criou porque já existe

#Pegar chave pública
@app.route("/getPublicKey", methods=["GET"])
def public_key():
    private_key, public_key = rsa.get_rsa_keys()
    return jsonify({"public_key": public_key.decode("utf-8")}), 200

#Pega o salt no login
@app.route("/getSalt", methods=["POST"])
def get_salt():
    dados = request.json
    nome = dados.get("nome")
    resultado = crud.get_salt_login(nome)

    if resultado.get("status"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 400
    
#Login (POST -> usuário)
@app.route("/login", methods=["POST"])
def login_api():
    dados = request.json #dados criptografados

    payload = rsa.rsa_decode_API(dados)
    nome = payload.get("nome") 
    senha = payload.get("senha") 

    resultado = crud.login(nome, senha)
    
    if resultado.get("status"):
        return jsonify({"status": True }), 200 #ok
    else: 
        return jsonify({"status": False}), 401 #credenciais inválidas
    
#Criar senha (POST -> senha)
@app.route("/createPassword", methods=["POST"])
def create_password_api():
    dados = request.json
    payload = rsa.rsa_decode_API(dados)

    nome = payload.get("nome")
    plataforma = payload.get("plataforma")
    senha = payload.get("senha")
    salt = payload.get("salt")
    tag = payload.get("tag")
    nonce = payload.get("nonce")

    resultado = crud.create(nome, plataforma, senha, salt, tag, nonce)
    if resultado.get("status"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 409 #Jé existe
    
#Ler senhas (GET -> senha)
@app.route("/readPassword", methods=["POST"])
def read_passwords_api():
    dados = request.json
    nome = dados.get("nome")
    payload = crud.read(nome)

    if not payload.get("status"):
        return jsonify(payload), 404
    else:
        return jsonify({"status": True, "registros": payload["registros"]})
    
#Atualizar senha (PUT ou PATH -> senha)
@app.route("/updatePassword", methods=["PATCH"])
def update_api():
    dados = request.json
    payload = rsa.rsa_decode_API(dados)

    nome = payload.get("nome")
    plataforma = payload.get("plataforma")
    nova_senha = payload.get("senha")
    novo_salt = payload.get("salt")
    nova_tag = payload.get("tag")
    novo_nonce = payload.get("nonce")

    resultado = crud.update(nome, plataforma, nova_senha, novo_salt, nova_tag, novo_nonce)

    if resultado.get("status"):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 404 #nada encontrado (nenhum registro encontrado)
    
#Deletar senha
@app.route("/deletePassword", methods=["DELETE"])
def delete_api():
    dados = request.json
    nome = dados.get("nome")
    plataforma = dados.get("plataforma")

    resultado = crud.delete(nome, plataforma)
    if resultado.get("status"):
        return jsonify(resultado), 200
    else: 
        return jsonify(resultado), 404 #nada deletado (nenhum registro encontrado)
    

if __name__ == "__main__":
    init_db.create_schema()
    init_db.create_table_usuary()
    init_db.create_table_password()
    app.run(debug=True)