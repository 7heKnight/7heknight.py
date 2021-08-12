from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import *
from hashlib import md5, sha256
from Crypto.Cipher import AES
from base64 import *
import platform
import sys
import os

class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('UTF-8')).digest()

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data,
            AES.block_size)))

def hashing(data):
    sha_hash = sha256(data).hexdigest().encode('UTF-8')
    sha_hash = str(sha_hash).replace("b'", '').replace("'", '')
    return sha_hash

def user_input():
    file_name = ''
    type_of_data = input('[*] Choosing type of data to encrypt f/s (file/string): ').lower()

    # If File type, will execute this
    if 'f' in type_of_data:
        file_name = input('[*] Input file name to encrypt: ')
        if not os.path.isfile(file_name):
            sys.exit('[-] Cannot find the file.')
        data = open(file_name, 'rb').read()

    # If String type, will execute this
    elif 's' in type_of_data:
        data = input('[*] Input the data to encrypt: ').encode('UTF-8')
    else:
        sys.exit('[-] Wrong type! Terminated.')
    # USER INPUT SECRET KEY
    aes_key = input('[*] Enter security key: ')
    return data, aes_key, file_name, type_of_data

if __name__=='__main__':
    data, aes_key, file_name, type_of_data = user_input()
    cipher = AESCipher(aes_key).encrypt(data)
    hash_data = hashing(data)
    hash_key = hashing(aes_key.encode('UTF-8'))
    print('========== RESULT ==========')
    if 'f' in type_of_data:
        os.remove(file_name)
        f = open(file_name + '.aes', 'wb')
        f.write(cipher)        
        if platform.system() == 'Windows':
            print(f'[+] Encrypted data save in {os.getcwd()}\\{file_name}.aes')
        else:
            print(f'[+] Encrypted data save in {os.getcwd()}/{file_name}.aes')
        print(f'[+] Hashed data: {hash_data}')
        print(f'[+] Hashed key: {hash_key}')
    elif 's' in type_of_data:
        print(f'[+] Encrypted Data: {cipher.decode("UTF-8")}')
        print(f'[+] Hashed data: {hash_data}')
        print(f'[+] Hashed key: {hash_key}')
