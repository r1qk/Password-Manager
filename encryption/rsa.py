import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json

def get_rsa_keys():
    if not os.path.exists("pm1/keys"):
        os.makedirs("keys", exist_ok=True) #cria a pasta caso não exista e não da erro se já criou antes

    if not os.path.exists("keys/private_key.pem") or os.path.exists("keys/public_key.pem"):
        chave_AES = RSA.generate(2048) #senha aes para sessão
        with open ("keys/private_key.pem", "wb") as pk:
            pk.write(chave_AES.export_key()) #senha privada
        with open ("keys/public_key.pem", "wb") as pk:
            pk.write(chave_AES.publickey().export_key()) #senha pública

    #Se já existe, só carrega
    with open ("keys/private_key.pem", "rb") as pk:
        private_key = RSA.import_key(pk.read()) #transforma em objeto python
    with open ("keys/public_key.pem", "rb") as pk:
        public_key = pk.read() #volta em string/bytes

    return private_key, public_key

#descriptografar rsa na api
def rsa_decode_API(dados):
    #hex -> bytes
    key_aes_encrypted = bytes.fromhex(dados["key_aes"])
    nonce = bytes.fromhex(dados["nonce"])
    tag = bytes.fromhex(dados["tag"])
    data = bytes.fromhex(dados["data"])

    #carregar chave privada
    with open("keys/private_key.pem", "rb") as pk:
        private_key_pem = pk.read()

    private_key = RSA.import_key(private_key_pem)

    #descriptografar chave aes com rsa
    cipher_rsa = PKCS1_OAEP.new(private_key)
    chave_aes = cipher_rsa.decrypt(key_aes_encrypted)

    #descriptografar payload com aes
    cipher_aes = AES.new(chave_aes, AES.MODE_EAX, nonce=nonce)
    payload_bytes = cipher_aes.decrypt_and_verify(data, tag)
    payload = json.loads(payload_bytes.decode("utf-8"))

    return payload       