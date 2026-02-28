from db.db import get_connect
import encryption.criptografia as criptografia

#CREATE(INSERT) | Criar conta na tabela de usuários (evitando duplicatas)
def create_account(nome, senha_m, salt):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT 1 FROM password_manager.usuarios WHERE nome = %s;', (nome,))

    if cursor.fetchone():
        cursor.close()
        conexao.close()
        return {"status": False, "mensagem": "Essa conta já existe!"}#já existe
    else:
        cursor.execute('INSERT INTO password_manager.usuarios (nome, senha_mestra, salt) VALUES (%s, %s, %s);', (nome, senha_m, salt))
        # cursor.execute('INSERT INTO password_manager.usuarios (nome, senha_mestra) VALUES (%s, %s);', (nome, senha_m))
        conexao.commit()
        cursor.close()
        conexao.close()
        return {"status": True, "mensagem": "Conta criada!"} #essa conta foi criada agora

#LOGIN (validação de usuário utilizando select)
def login(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()
    cursor.execute('SELECT senha_mestra FROM password_manager.usuarios WHERE nome = %s;', (nome,))
    resultado = cursor.fetchone()
    if resultado is None:
        cursor.close()
        conexao.close()
        return {"status": False, "mensagem": "Nome de usuário ou senha inválidos!"}

    else:
        senha_mestra_bd = resultado[0]
        if senha_mestra_bd == senha_m:
            cursor.close()
            conexao.close()
            return {"status": True, "mensagem": f"Bem vindo(a), {nome}!"}
        else:
            cursor.close()
            conexao.close()
            return {"status": False, "mensagem": "Senha inváldida!"}
        

def get_salt_login(nome):
    conexao = get_connect()
    cursor = conexao.cursor()
    cursor.execute('SELECT salt FROM password_manager.usuarios WHERE nome = %s;', (nome,))
    resultado = cursor.fetchone()
    if resultado is None:
        cursor.close()
        conexao.close()
        return {"status": False}
    
    resultado = resultado[0]
    cursor.close()
    conexao.close()
    return {"status": True, "salt": resultado}
    


#CREATE(INSERT) | Criar registro na tabela de senhas (evitar duplicatas)
def create(nome_login, plataforma_input, senha, salt, tag, nonce):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s', (nome_login,))
    id_usuario = cursor.fetchone()[0] # = cursor.fetchall()[0][0]
    if id_usuario is None:
        cursor.close()
        conexao.close()
        return {"status": False}
    
    cursor.execute('INSERT INTO password_manager.senhas (id_usuario, plataforma, senha, salt, nonce, tag) VALUES (%s, %s, %s, %s, %s, %s);', (id_usuario, plataforma_input, senha, salt, nonce, tag))
    conexao.commit()

    cursor.close()
    conexao.close()

    return {"status": True, "mensagem": "Senha criada!"}

#READ | Ler  os dados
def read(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_usuario = cursor.fetchone()[0]

    if not id_usuario:
        cursor.close()
        conexao.close()
        return {"status": False, "mensagem": "Nenhuma senha encontrada"}
    
    cursor.execute('SELECT senhas.plataforma, senhas.senha, senhas.salt, senhas.nonce, senhas.tag FROM password_manager.senhas WHERE id_usuario = %s;', (id_usuario,))
    registros = cursor.fetchall()

    if not registros: #lista vazia do fetchall
        cursor.close()
        conexao.close()
        return {"status": False, "mensagem": "Nenhuma senha encontrada"}

    cursor.close()
    conexao.close()
    return {"status": True, "registros": registros}




#UPDATE | Atualizar os dados
def update(nome_login, plataforma, nova_senha, novo_salt, nova_tag, novo_nonce):
    conexao = get_connect()
    cursor = conexao.cursor()
    #Selecionar id_usuario a partir do nome

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchone()[0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        return {"status": False, "mensagem": "Plataforma não encontrada, nenhuma senha foi alterada"}
    else:
        cursor.execute('UPDATE password_manager.senhas SET senha = %s, salt = %s, tag = %s, nonce = %s WHERE plataforma = %s AND id_usuario = %s;', (nova_senha, novo_salt, nova_tag, novo_nonce, plataforma, id_salvo))
        conexao.commit()      
        cursor.close()
        conexao.close()
        return {"status": True, "mensagem": "Senha atualizada!"}



#DELETE | Deletar os dados
def delete(nome_login, plataforma):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchall()[0][0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close() 
        return {"status": False, "mensagem": "Plataforma não encontrada!"}
    else:
        cursor.execute('DELETE FROM password_manager.senhas WHERE plataforma = %s AND id_usuario = %s;', (plataforma, id_salvo))
        conexao.commit()
        cursor.close()
        conexao.close() 
        return {"status": True, "mensagem": "Senha deletada"}