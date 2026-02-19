#FRONTEND
import pwinput
import init_db
import crud


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
    init_db.create_schema()
    init_db.create_table_usuary()
    init_db.create_table_password()
    while True:
        opcao = menu1()
        match opcao:
            case 1: #Logar
                    nome_login = input("Nome de usuário: ")
                    senha_m = pwinput.pwinput(prompt="Digite sua senha: ")
                    validacao = init_db.login(nome_login, senha_m)
                    if not validacao:
                        print("Nome de usuário ou senha inválido!\n")
                    else:
                        print(f"Bem vindo, {nome_login}!\n")
                        while True:
                            opcao2 = menu2() #CRUD
                            if opcao2 == 1:
                                init_db.create(nome_login)
                            if opcao2 == 2:
                                init_db.read(nome_login)
                            if opcao2 == 3:
                                init_db.update(nome_login)
                            if opcao2 == 4:
                                init_db.delete(nome_login)
                            if opcao2 == 5:
                                print("Voltando para o menu.\n")
                                break

            case 2: #Criar nova conta
                nome = input("Nome de usuário: ")
                senha_m = pwinput.pwinput(prompt="Digite sua senha: ")
                init_db.create_account(nome, senha_m)
  
            case 3: #Sair
                print("Fim do programa! Reinicie o código para recomeçar!\n")
                break

if __name__ == "__main__":
    main()