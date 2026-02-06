#backend
from db import get_connect
from mysql.connector import Error

# conexao = get_connect() #não sei se precisa aqui
# cursor = conexao.cursor()

#CREATE | Criar Database
def create_schema():
    try: 
        conexao = get_connect()

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS password_manager;')
            conexao.commit()
    
    except Error:
        print("Não foi possível conectar")

    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()

#CREATE | Tabela de usuários
def create_table_usuary():
    try: 
        conexao = get_connect()

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.usuarios (id_usuario INTEGER PRIMARY KEY auto_increment, nome VARCHAR(250), senha_mestra VARCHAR(250));')
            conexao.commit()
    
    except Error:
        print("Não foi possível conectar")

    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()


#CREATE | Criar tabela de senhas
def create_table_password():
    try: 
        conexao = get_connect()

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.senhas (id_usuario INT, plataforma VARCHAR(250), senha VARCHAR(250));')
            conexao.commit()

    
    except Error:
        print("Não foi possível conectar")

    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()

#CREATE(INSERT) | Criar conta na tabela de usuários (evitando duplicatas)

def create_account(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()

    comando = 'SELECT 1 FROM password_manager.usuarios WHERE nome = %s;'
    cursor.execute(comando, (nome,))
    if cursor.fetchone():
        print("Essa conta já existe!\n")
    else:
        comando2 = 'INSERT INTO password_manager.usuarios (nome, senha_mestra) VALUES (%s, %s);'
        cursor.execute(comando2, (nome, senha_m))
        conexao.commit()
        print("Conta criada!\n")

    cursor.close()
    conexao.close()

#LOGIN 
def login(nome, senha_m):
    conexao = get_connect()
    cursor = conexao.cursor()
    cursor.execute('SELECT 1 FROM password_manager.usuarios WHERE nome = %s and senha_mestra = %s', (nome, senha_m))
    if cursor.fetchone() is None:
        # print("Nome de usuário ou senha inválido!\n")
        validacao = False
    else:
        # print(f"Bem vindo, {nome}!\n")
        validacao = True

    cursor.close()
    conexao.close()

    return validacao

        



#CREATE(INSERT) | Criar registro na tabela de senhas (evitar duplicatas)
def create(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()

    plataforma = input("Digite a plataforma da senha: ")
    senha = input("Digite a senha: ")

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s', (nome_login,))
    id_usuario = cursor.fetchall()[0][0]
    cursor.execute('INSERT INTO password_manager.senhas (id_usuario, plataforma, senha) VALUES (%s, %s, %s);', (id_usuario, plataforma, senha))
    conexao.commit()
    print("Senha inserida!\n")

    cursor.close()
    conexao.close()

#READ | Ler  os dados
def read(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_usuario = cursor.fetchone()[0]

    cursor.execute('SELECT senhas.plataforma, senhas.senha FROM password_manager.senhas WHERE id_usuario = %s;', (id_usuario,))
    resultado = cursor.fetchall()

    if not resultado: #lista vazia do fetchall
        print("Não há nenhuma senha registrada.")
    else:
        print()
        print("-"*6, "Senhas registradas", "-"*6)
        for registro in resultado:
            print(f"Plataforma: {registro[0]} | Senha: {registro[1]}")

    print()
    cursor.close()
    conexao.close()


#UPDATE | Atualizar os dados
def update(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()
    #Selecionar id_usuario a partir do nome
    plataforma = input("Digite a plataforma que quer atualizar: ")

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchall()[0][0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))

    if cursor.fetchone() is None:
        print("Plataforma não encontrada!\n")
    else:
        nova_senha = input("Digite a nova senha: ")
        cursor.execute('UPDATE password_manager.senhas SET senha = %s WHERE plataforma = %s AND id_usuario = %s;', (nova_senha, plataforma, id_salvo))
        conexao.commit()
        print("Senha atualizada!\n")
    cursor.close()
    conexao.close()


#DELETE | Deletar os dados
def delete(nome_login):
    conexao = get_connect()
    cursor = conexao.cursor()

    plataforma = input("Digite a plataforma do registro que quer deletar: ")

    cursor.execute('SELECT id_usuario FROM password_manager.usuarios WHERE nome = %s;', (nome_login,))
    id_salvo = cursor.fetchall()[0][0]
    cursor.execute('SELECT 1 FROM password_manager.senhas WHERE id_usuario = %s AND plataforma = %s;', (id_salvo, plataforma))
    if cursor.fetchone() is None:
        print("Plataforma não encontrada!\n")
    else:
        cursor.execute('DELETE FROM password_manager.senhas WHERE plataforma = %s AND id_usuario = %s;', (plataforma, id_salvo))
        conexao.commit()
        print("Registro deletado!\n")

    cursor.close()
    conexao.close() 
    


