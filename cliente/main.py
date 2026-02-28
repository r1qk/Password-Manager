#FRONTEND
import pwinput
import encryption.criptografia as cripto
import requests

def menu1():
    print("-"*5, " Bem vindo ", "-"*5)
    print("1) Login\n2) Criar nova conta\n3) Sair")
    while True:
        opcao = input("Escolha uma opção: ")
        if opcao.isdigit() and 1 <= int(opcao) < 4:
            break
        else:
            print("Tente novamente\n")

    return int(opcao)

def menu2():
    print("--- Digite o número equivalente ao que quer fazer ---")
    print("1) Adicionar uma senha no banco\n2) Listar as senhas do banco\n3) Atualizar uma informação do banco\n4) Deletar uma senha do banco\n5) Voltar para o Menu")
    while True:
        opcao2 = input("Escolha uma opção: ")
        if opcao2.isdigit() and 1 <= int(opcao2) < 6:
            break
        else:
            print("Tente novamente\n")

    return int(opcao2)
        

def main():
    while True:
        opcao = menu1()
        match opcao:
            case 1: #Logar
                    response = requests.get("http://localhost:5000/getPublicKey") 

                    # print("STATUS:", response.status_code)
                    # print("HEADERS:", response.headers)
                    # print("TEXTO:", response.text)

                    public_key = response.json()["public_key"] #JSON -> dicionário python | public_key


                    
                    nome_login = input("Nome de usuário: ")
                    senha_m = pwinput.pwinput(prompt="Digite sua senha: ")
                    payload_nome = {
                        "nome": nome_login
                    }
                    get_salt = requests.post("http://localhost:5000/getSalt", json=payload_nome)
                    dados_salt = get_salt.json()
                    if dados_salt["status"]:
                        salt = dados_salt["salt"]
                    else:
                        print("Usuário não encontrado!\n")
                        continue #Próximo loop
                    
                    senha_m_hash = cripto.login_hash(senha_m, salt)
                    payload = {
                        "nome": nome_login,
                        "senha": senha_m_hash
                    }
                    payload_rsa = cripto.rsa_encode_payload(public_key, payload)
                    validacao = requests.post("http://localhost:5000/login", json=payload_rsa) #transforma em json e depois em dicionário automaticamente
                    if validacao.status_code != 200:
                        print("Nome de usuário ou senha inválido!\n")
                    else:
                        print(f"Bem vindo, {nome_login}!\n")
                        while True:
                            opcao2 = menu2() #CRUD
                            if opcao2 == 1: #Criar 
                                plataforma = input("Digite a plataforma que quer adicionar: ")
                                senha = input("Digite a senha que quer adicionar a essa plataforma: ")
                                senha_cripto, salt, tag, nonce = cripto.encode_senhas(senha, senha_m_hash)
                                payload2 = {
                                    "nome": nome_login,
                                    "plataforma": plataforma,
                                    "senha": senha_cripto,
                                    "salt": salt,
                                    "tag": tag,
                                    "nonce": nonce
                                }
                                payload_rsa2 = cripto.rsa_encode_payload(public_key, payload2)
                                validacao2 = requests.post("http://localhost:5000/createPassword", json=payload_rsa2)

                                if validacao2.status_code == 200 or validacao2.status_code == 201:
                                    print("Registro criado com sucesso!\n")
                                else:
                                    print(f"Erro inesperado! STATUS: {validacao2.status_code}\nTEXTO: {validacao2.text}")
                                

                            if opcao2 == 2: #Leitura
                                response = requests.post("http://localhost:5000/readPassword", json={"nome": nome_login})
                                dados_cripto = response.json()

                                if not dados_cripto.get("status"): 
                                    print("Nenhuma senha encontrada.\n")
                                    continue
                                else:
                                    registros = dados_cripto.get("registros")
                                    for registro in registros: #registro é uma tupla
                                        senha_decoded = cripto.decode_senhas(registro, senha_m_hash)
                                        print(f"Plataforma: {registro[0]} | Senha: {senha_decoded}")
                                    print("")

                            if opcao2 == 3: #Atualizar
                                plataforma = input("Digite a plataforma que quer alterar a senha: ")
                                nova_senha = input("Digite a nova senha: ")
                                senha_cripto, salt, tag, nonce = cripto.encode_senhas(nova_senha, senha_m_hash)
                                payload2 = {
                                    "nome": nome_login,
                                    "plataforma": plataforma,
                                    "senha": senha_cripto,
                                    "salt": salt,
                                    "tag": tag,
                                    "nonce": nonce
                                }
                                payload_rsa2 = cripto.rsa_encode_payload(public_key, payload2)
                                validacao2 = requests.patch("http://localhost:5000/updatePassword", json=payload_rsa2)
                                if validacao2.status_code != 200:
                                    print("Plataforma não encontrada, nenhuma senha foi alterada\n")
                                else:
                                    print("Senha atualizada!\n")


                            if opcao2 == 4: #Deletar
                                plataforma = input("Digite a o nome da plataforma para deletar um registro: ")
                                payload = {
                                    "nome": nome_login,
                                    "plataforma": plataforma
                                }
                                validacao2 = requests.delete("http://localhost:5000/deletePassword", json=payload)
                                if validacao2.status_code != 200:
                                    print("Plataforma não encontrada, nenhum registro foi deletado!\n")
                                else:
                                    print("Registro deletado!\n")
                                
                            if opcao2 == 5:
                                print("Voltando para o menu.\n")
                                break

            case 2: #Criar nova conta
                nome = input("Nome de usuário: ")
                senha_m = pwinput.pwinput(prompt="Digite sua senha: ")
                senha_m_hash, salt_hash = cripto.criptografar_sm(senha_m)

                response = requests.get("http://localhost:5000/getPublicKey")
                public_key = response.json()["public_key"] #JSON -> dicionário python | public_key

                payload = {
                    "nome": nome,
                    "senha": senha_m_hash,
                    "salt": salt_hash
                }

                payload_rsa = cripto.rsa_encode_payload(public_key, payload)
                validacao = requests.post("http://localhost:5000/createAccount", json=payload_rsa)

                if validacao.status_code != 201:
                    print("Essa conta já existe.\n")
                else:
                    print("Conta criada!\n")

                
                
  
            case 3: #Sair
                print("Fim do programa! Reinicie o código para recomeçar!\n")
                break

if __name__ == "__main__":
    main()




