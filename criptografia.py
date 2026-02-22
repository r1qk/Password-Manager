from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hashlib

#Função que cria o Hash + salt da senha mestra na tabela de usuarios
def criptografar_sm (senha_mestra):
    senha = senha_mestra.encode('utf-8') #senha mestra em bytes
    salt = get_random_bytes(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha3-512',
        senha,
        salt,
        dklen=32,
        iterations= 100000
    )
    #o resultado volta em bytes, precisa transformar em string hexadecimal legível
    hash_hex = hash_bytes.hex() 
    salt_hex = salt.hex() 
    return hash_hex, salt_hex #senha e salt criptografado

#Função que verifica se o usuário e a senha são válidos
def login_hash(senha_input, salt):
    salt = bytes.fromhex(salt) #transformando em byte
    senha = senha_input.encode('utf-8') #senha mestra em bytes
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha3-512',
        senha,
        salt,
        dklen=32,
        iterations= 100000
    )
    hash_hex_try = hash_bytes.hex() 
    return hash_hex_try

# #Criptografando senhas adicionadas e substituídas
# def encode_senhas(senha, senha_mestra): #create senhas
#     senha_mestra = senha_mestra.encode('utf-8') #senha mestra em bytes
#     senha = senha.encode('utf-8')
#     salt = get_random_bytes(16)
#     chave = PBKDF2(senha_mestra, salt, 32, count=100000)
#     cipher = AES.new(chave, AES.MODE_EAX)
#     senha_encoded, tag = cipher.encrypt_and_digest(senha) #senha criptografada
#     nonce = cipher.nonce
#     # retornar senha_encoded, salt, tag e nonce
#     return senha_encoded.hex(), salt.hex(), tag.hex(), nonce.hex()

#Criptografando senhas adicionadas e substituídas
def encode_senhas(senha, senha_mestra): #create senhas
    senha_mestra = bytes.fromhex(senha_mestra) #senha mestra em bytes
    senha = senha.encode('utf-8')
    salt = get_random_bytes(16)
    chave = PBKDF2(senha_mestra, salt, 32, count=100000)
    cipher = AES.new(chave, AES.MODE_EAX)
    senha_encoded, tag = cipher.encrypt_and_digest(senha) #senha criptografada
    nonce = cipher.nonce
    # retornar senha_encoded, salt, tag e nonce
    return senha_encoded.hex(), salt.hex(), tag.hex(), nonce.hex()

#Descriptografando senhas adicionadas
def decode_senhas(tupla, senha_mestra): #read
    senha_encoded = bytes.fromhex(tupla[1])
    salt = bytes.fromhex(tupla[2])
    nonce = bytes.fromhex(tupla[3])
    tag = bytes.fromhex(tupla[4])
    
    senha_mestra = bytes.fromhex(senha_mestra)
    nova_chave = PBKDF2(senha_mestra, salt, 32, count=100000)
    cipher = AES.new(nova_chave, AES.MODE_EAX, nonce)
    senha_decoded = cipher.decrypt_and_verify(senha_encoded, tag)
    return senha_decoded.decode('utf-8')


