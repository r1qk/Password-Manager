from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
import json
import hashlib

#Função que cria o Hash + salt da senha mestra na tabela de usuarios
def criptografar_sm(senha_mestra):
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

#criptografando com rsa para login no cliente
def rsa_encode_payload(public_key, payload): #chave pública em string

    public_key_obj = RSA.import_key(public_key.encode("utf-8")) #transformando em objeto tipo RSA.Rsakey
    chave_sessao = get_random_bytes(32) #chave aes
    payload_json = json.dumps(payload).encode("utf-8")
    cipher = AES.new(chave_sessao, AES.MODE_EAX) #criptografia do payload com aes
    dados_criptografados, tag = cipher.encrypt_and_digest(payload_json)
    nonce = cipher.nonce

    cipher_rsa = PKCS1_OAEP.new(public_key_obj)
    chave_sessao_encoded = cipher_rsa.encrypt(chave_sessao)

    return {
        "key_aes": chave_sessao_encoded.hex(),
        "tag": tag.hex(),
        "nonce": nonce.hex(),
        "data": dados_criptografados.hex()
    }
