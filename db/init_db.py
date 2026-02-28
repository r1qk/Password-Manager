#backend
from db.db import get_connect
from mysql.connector import Error

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
            # cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.usuarios (id_usuario INTEGER PRIMARY KEY auto_increment, nome VARCHAR(250), senha_mestra VARCHAR(250));')
            cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.usuarios (id_usuario INTEGER PRIMARY KEY auto_increment, nome VARCHAR(250), senha_mestra VARCHAR(80) NOT NULL, salt VARCHAR(80) NOT NULL);')
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
            # cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.senhas (id_usuario INT, plataforma VARCHAR(250), senha VARCHAR(250));')
            cursor.execute('CREATE TABLE IF NOT EXISTS password_manager.senhas (id_usuario INT, plataforma VARCHAR(250), senha VARCHAR(256), salt VARCHAR(80), nonce VARCHAR(80), tag VARCHAR(80));')
            conexao.commit()

    
    except Error:
        print("Não foi possível conectar")

    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()