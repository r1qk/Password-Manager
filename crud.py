from db import get_connect

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
        cursor.execute('INSERT INTO password_manager.usuarios (nome, senha_mestra) VALUES (%s, %s);', (nome, senha_m))
        conexao.commit()
        cursor.close()
        conexao.close()
        return {"sucesso": True, "mensagem": "Conta criada!"} #essa conta foi criada agora

#LOGIN (validação de usuário utilizando select)
def login(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()
    cursor.execute('SELECT 1 FROM password_manager.usuarios WHERE nome = %s and senha_mestra = %s', (nome, senha_m))
    if cursor.fetchone() is None:
        # print("Nome de usuário ou senha inválido!\n")
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Nome de usuário ou senha inválido!"}

    else:
        # print(f"Bem vindo, {nome}!\n")
        cursor.close()
        conexao.close()
        return {"sucesso": True, "mensagem": f"Bem vindo(a), {nome}!"}


#CREATE(INSERT) | Criar registro na tabela de senhas (evitar duplicatas)
def create(nome_login, plataforma, senha):
    conexao = get_connect()
    cursor = conexao.cursor()

    # plataforma = input("Digite a plataforma da senha: ")
    # senha = input("Digite a senha: ")

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s', (nome_login,))
    id_usuario = cursor.fetchone()[0] # = cursor.fetchall()[0][0]
    cursor.execute('INSERT INTO password_manager.senhas (id_usuario, plataforma, senha) VALUES (%s, %s, %s);', (id_usuario, plataforma, senha))
    conexao.commit()

    cursor.close()
    conexao.close()

    return {"sucesso": True, "mensagem": "Senha criada!"}

#READ | Ler  os dados
def read(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_usuario = cursor.fetchone()[0]

    if not id_usuario:
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "ID não encontrado"}

    cursor.execute('SELECT senhas.plataforma, senhas.senha FROM password_manager.senhas WHERE id_usuario = %s;', (id_usuario,))
    resultado = cursor.fetchall()

    # if not resultado: #lista vazia do fetchall
    #     return {"sucesso": False, "mensagem": "Nenhuma senha encontrada"}
    # else:
    #     return {"sucesso": True, "senhas": resultado}

    return {"sucesso": True, "senhas": resultado, "mensagem": "Nenhuma senha encontrada" if not resultado else "Exibindo senhas"}




#UPDATE | Atualizar os dados
def update(nome_login, plataforma, nova_senha):
    conexao = get_connect()
    cursor = conexao.cursor()
    #Selecionar id_usuario a partir do nome

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchone()[0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))

    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        return {"sucesso": False, "mensagem": "Id não encontrado, nenhuma senha foi alterada"}
    else:
        cursor.execute('UPDATE password_manager.senhas SET senha = %s WHERE plataforma = %s AND id_usuario = %s;', (nova_senha, plataforma, id_salvo))
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