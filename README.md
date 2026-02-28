# Projeto - Password Manager
Este repositório contém o projeto Password Manager, um programa que permite
o usuário armazenar suas senhas dentro de um cofre em um servidor local. O 
trabalho foi realizado com a linguagem Python, protocolo HTTP e FLASK, utilizando 
criptografia híbrida para o transporte de dados e criptografia SHA3-512 + SALT 
e AES-256 para o armazenamento de informações no banco de dados, enquanto o Sistema de
gerenciamento de banco de dados foi o MySQL, recorrendo ao uso da linguagem
SQL para fazer alterações no banco de dados.

## 1) Preparando o ambiente
Esse projeto funciona em um servidor local, mesmo assim, é importante preparar 
o ambiente em que o projeto irá rodar. Para isso: é necessário:

- Instalar e configurar o MySQL;
- Instalar as dependências (bibliotecas utilizadas durante o projeto);
- Configurar o arquivo .env. 

### 1.1) Baixando o projeto
Para baixar o projeto na sua máquina, inicialmente você clica no botão **code** e depois em download zip. Caso tenha o git instalado na máquina, você pode digitar o código abaixo no diretório que quer
salvar o arquivo para baixar o programa.

```
git clone https://github.com/r1qk/Password-Manager.git
```
### 1.2) MySQL
É necessário que tenha o MySQL instalado no seu computador. Ele é o Sistema de gerenciamento de 
banco de dados que armazena o banco de dados utilizado nesse projeto. 

### 1.3) .env
Crie um arquivo .env no diretório que salvou o projeto. Aqui é onde você coloca suas variáveis
de ambiente, informações sensíveis sobre o MySQL que serão utilizadas durante o projeto, sendo elas: 
- HOST (endereço onde o banco de dados será executado): iremos utilizar o endereço local, localhost;
- USER: nome do usuário configurado durante a instalação do MySQL;
- PASSWORD: senha configurada durante a instalação do MySQL.

Exemplo:
```
HOST=localhost
USER=root
PASSWORD=senha_do_usuario
```
Observação: durante o desenvolvimento, é comum nomear variáveis de ambiente com letras maiúsculas.

### 1.4) Criar ambiente virtual (opcional)
Você pode instalar o projeto e já utilizá-lo no python global, mas é uma boa prática criar ambientes
virtuais para esses projetos, evitando conflitos e garantir que o projeto funcione igual em qualquer
máquina. Para isso, crie um ambiente virtual seguindo o código abaixo no terminal dentro do diretório
raiz.  
Cria o ambiente virtual:
```
python -m venv venv
```
Ativa o ambiente virtual:
```
venv\Scripts\activate.bat
```
### 1.5) Baixando o requirements
O arquivo requirements.txt é um arquivo que contém as bibliotecas usadas durante o projeto. É 
importante que você tenha todas elas instaladas para que o código funcione normalmente. Após 
instalar o repositório, abra o terminal e instale a dependência reqs. Após isso, você pode 
instalar o requirements.txt, assim todas as bilibotecas serão instaladas automaticamente na sua
máquina, seja no python global ou ambiente virtual.  
Baixando a dependência reqs:
```
pip install reqs
```
Baixando o requirements.txt:
```
pipreqs . --force --encoding utf-8
```
### 1.6) Rodando o código
Para testar o código, é importante abrir duas linhas de comando no diretório raiz, por exemplo o 
CMD. Em uma delas, primeiro você deve rodar o arquivo da API utilizada, e somente depois rodar o arquivo principal, main.py. Para isso, digite o código abaixo no diretório raiz.  
CMD 1: Rodar a API
```
python -m api.api
```
CMD 2: Rodar o arquivo main
```
python -m cliente.main
```
Após todos os passos anteriores estiverem completos, você pode testar o projeto. 

## 2) Como o projeto funciona
O programa começa com um menu com as opções: login, criar conta e sair. 
### 2.1) Criar conta
O usuário digita um nome e uma senha. Essa senha é criptografada com um algoritmo de segurança PBKDF2, além de gerar um salt, código que, ao se alinhar com a senha criptografada pelo PBKDF2, gera uma senha hasheada, ou seja, uma senha que não pode ser decodificada. O nome de usuário, a senha hash e o salt são tratados como informações a serem enviadas para a API (payload), o payload é criptografado através de uma chave temporária AES, e essa chave AES é criptografada com RSA, um tipo de criptografia assimétrica que utiliza chaves públicas e privadas. Após o transporte de dados com criptografia híbrida (chave AES + RSA) ser realizado, as informações são salvas na tabela usuários do banco de dados.
```
-----  Bem vindo  -----
1) Login
2) Criar nova conta
3) Sair
Escolha uma opção:
```
### 2.2 Login 
O usuário digita um nome e uma senha de login. O nome é verificado dentro do banco de dados e, caso ele exista, um salt é retornado. É utilizado o mesmo algoritimo PBKDF2 com o salt retornado para criar uma senha hash. Se a senha hash for a mesma do banco de dados, o usuário consegue logar no sistema, e o próximo menu é liberado.
### 2.3 CRUD 
O termo CRUD consiste em create, read, update e delete. Aqui é onde o segundo menu é liberado e o usuário pode modificar seu gerenciador de senhas.  
**1. Create (criar):** O usuário digita uma plataforma e uma senha que quer adicionar. Se a plataforma já foi cadastrada no gerenciador, a senha não é adicionada, caso contrário, a senha será adicionada no programa. Vale mencionar que a senha é adicionada com criptografia AES-256, ou seja, ela pode ser revertida para a exibição dos dados.  
**2. Read (ler):** Aqui, todas as senhas são decodificadas pelo AES-256 e são exibidas pelo usuário. Para a decodificação acontecer, são usados salt, tag e nonce, informações geradas pelo AES-256 para a decodificação das senhas. Elas são salvas quando a senha é criada e adicionada no gerenciador.  
**3. Update (atualizar):** O usuário digita a plataforma que ele quer atualizar e digita a nova senha. A senha é enviada para a API e é escrita sobre a antiga senha.   
**4. Delete (excluir):** O usuário digita a plataforma da senha e a senha é excluída do banco de dados. Não só a senha, mas as outras informações (tag, nonce e salt) também são deletadas.
```
-----  Bem vindo  -----
1) Login
2) Criar nova conta
3) Sair
Escolha uma opção: 1
Nome de usuário: Riquelme
Digite sua senha: *******
Bem vindo, Riquelme!

--- Digite o número equivalente ao que quer fazer ---
1) Adicionar uma senha no banco
2) Listar as senhas do banco
3) Atualizar uma informação do banco
4) Deletar uma senha do banco
5) Voltar para o Menu
Escolha uma opção:
```
## 3) Organização
O gerenciador de senhas (password manager) foi dividido em quatro diretórios, cada um deles com 
arquivos importantes para o projeto:
- **cliente (main.py):** onde o código o código funciona como frontend;
- **encryption (rsa.py, criptografia.py):** onde estão localizadas as criptografias usadas no lado do cliente, seja para codificar ou decodificar;
- **db (crud.py, init_db.py, db.py):** onde estão localizadas as funções da API e os dados do MYSQL, que trabalham com o SGBD;
- **api (api.py):** onde está localizada todos os endereços com as funções citadas acima, servindo como ponte entre o cliente e o banco de dados.
## 4) Libs utilizadas
- **pwinput:** usada para esconder a senha mestra que o usuário digita para logar;
- **requests:** biblioteca que permite o uso dos métodos HTTP, que permitem enviar informações para a API;
- **flask:** micro frame-work utilizado para a criação da API;
- **Crypto.cipher:** usada para implementar o AES (chave que criptografa e descriptografa payload) e PKCS1_OAEP (esquema de criptografia RSA assimétrica que criptografa a chave AES);
- **Crypto.Random:** gera bytes aleatórios seguros para a criptografia, importante para gerar salt e nonce;
- **Crypto.Protocol.KDF:** utilizado para implementar PBKDF2 (algoritmo de derivação de chaves) e gerar a chave AES da criptografia dos dados através da chave mestra do usuário;
- **Crypto.PublicKey:** utlizada para implementar a criptografia RSA;
- **json**: biblioteca nativa do python para serializar e desserializar () objetos.
    - serializar: transformar objeto python em sequência de bytes ou strings;
    - desserializar: transforma string ou bytes em projeto python.

- **hashlib:** biblioteca utilizada para o SHA3-512, hash que gera a senha mestra;
- **os:** biblioteca nativa do python usada para ler variáveis de ambientes, verificar arquivos, gerenciar diretórios;
- **dotenv**: usado para carregar automaticamente um arquivo .env;
- **mysql.connector:** biblioteca que permite a conexão entre python e MySQL. 
