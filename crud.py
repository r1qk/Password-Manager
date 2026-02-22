from db import get_connect
import criptografia

#CREATE(INSERT) | Criar conta na tabela de usuários (evitando duplicatas)
def create_account(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT 1 FROM password_manager.usuarios WHERE nome = %s;', (nome,))

    if cursor.fetchone():
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Essa conta já existe!"}#já existe
    else:
        senha_m_hash, salt_hash = criptografia.criptografar_sm(senha_m)
        cursor.execute('INSERT INTO password_manager.usuarios (nome, senha_mestra, salt) VALUES (%s, %s, %s);', (nome, senha_m_hash, salt_hash))
        # cursor.execute('INSERT INTO password_manager.usuarios (nome, senha_mestra) VALUES (%s, %s);', (nome, senha_m))
        conexao.commit()
        cursor.close()
        conexao.close()
        return {"sucesso": True, "mensagem": "Conta criada!"} #essa conta foi criada agora

#LOGIN (validação de usuário utilizando select)
def login(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()
    cursor.execute('SELECT salt FROM password_manager.usuarios WHERE nome = %s;', (nome,))
    resultado = cursor.fetchone()
    if resultado is None:
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Nome de usuário ou senha inválido!"}

    else:
        salt_bd = resultado[0]
        nova_senha_hash = criptografia.login_hash(senha_m, salt_bd)
        cursor.execute('SELECT senha_mestra FROM password_manager.usuarios WHERE nome = %s;', (nome,))
        senha_correta = cursor.fetchall()[0][0]
        if nova_senha_hash == senha_correta:
            cursor.close()
            conexao.close()
            return {"sucesso": True, "mensagem": f"Bem vindo(a), {nome}!"}
        else:
            cursor.close()
            conexao.close()
            return {"sucesso": False, "mensagem": "Nome de usuário ou senha inválido!"}
    

#CREATE(INSERT) | Criar registro na tabela de senhas (evitar duplicatas)
def create(nome_login, plataforma, senha):
    conexao = get_connect()
    cursor = conexao.cursor()


    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s', (nome_login,))
    id_usuario = cursor.fetchone()[0] # = cursor.fetchall()[0][0]
    cursor.execute('SELECT senha_mestra FROM password_manager.usuarios WHERE nome = %s', (nome_login,))
    senha_mestra = cursor.fetchone()[0]

    senha_encoded, salt, tag, nonce = criptografia.encode_senhas(senha, senha_mestra)


    cursor.execute('INSERT INTO password_manager.senhas (id_usuario, plataforma, senha, salt, nonce, tag) VALUES (%s, %s, %s, %s, %s, %s);', (id_usuario, plataforma, senha_encoded, salt, nonce, tag))
    conexao.commit()

    cursor.close()
    conexao.close()

    return {"sucesso": True, "mensagem": "Senha criada!"}

#READ | Ler  os dados
def read(nome_login):
    senhas = [] #lista pra armazenar plataformas e senhas
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_usuario = cursor.fetchone()[0]

    if not id_usuario:
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "ID não encontrado"}

    cursor.execute('SELECT usuarios.senha_mestra FROM password_manager.usuarios WHERE id_usuario = %s;', (id_usuario,))
    senha_mestra = cursor.fetchone()[0]
    cursor.execute('SELECT senhas.plataforma, senhas.senha, senhas.salt, senhas.nonce, senhas.tag FROM password_manager.senhas WHERE id_usuario = %s;', (id_usuario,))
    resultado = cursor.fetchall()

    if not resultado: #lista vazia do fetchall
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Nenhuma senha encontrada"}
    else:
        for tupla in resultado:
            senha_decode = criptografia.decode_senhas(tupla, senha_mestra)
            registro = []
            registro.append(tupla[0])
            registro.append(senha_decode)
            senhas.append(registro)

        return {"sucesso": True, "Exibindo senhas": senhas}


#UPDATE | Atualizar os dados
def update(nome_login, plataforma, nova_senha):
    conexao = get_connect()
    cursor = conexao.cursor()
    #Selecionar id_usuario a partir do nome

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchone()[0]
    cursor.execute('SELECT senha_mestra FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    senha_mestra = cursor.fetchone()[0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Plataforma não encontrada, nenhuma senha foi alterada"}
    else:
        nova_senha_aes, salt, tag, nonce = criptografia.encode_senhas(nova_senha, senha_mestra)
        cursor.execute('UPDATE password_manager.senhas SET senha = %s, salt = %s, tag = %s, nonce = %s WHERE plataforma = %s AND id_usuario = %s;', (nova_senha_aes, salt, tag, nonce, plataforma, id_salvo))
        conexao.commit()      
        cursor.close()
        conexao.close()
        return {"sucesso": True, "mensagem": "Senha atualizada!"}



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
        return {"sucesso": False, "mensagem": "Plataforma não encontrada!"}
    else:
        cursor.execute('DELETE FROM password_manager.senhas WHERE plataforma = %s AND id_usuario = %s;', (plataforma, id_salvo))
        conexao.commit()
        cursor.close()
        conexao.close() 
        return {"sucesso": True, "mensagem": "Senha deletada"}