from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import *
from Crypto.Cipher import AES
from hashlib import md5
from base64 import *
import sys
import re
import os

class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).digest()

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def is_exist_file(file_name):
    try:
        open(file_name, 'r', encoding='UTF-8')
        return True
    except:
        return False

def user_input():
    file_name = ''
    type_of_data = input('[*] Choosing type of data to decrypt f/s (file/string): ').lower()

    # If File type, will execute this
    if 'f' in type_of_data:
        file_name = input('[*] Input file name to decrypt: ')
        if not is_exist_file(file_name):
            sys.exit('[-] Cannot find the file.')
        data = open(file_name, 'rb').read()

    # If String type, will execute this
    elif 's' in type_of_data:
        data = input('[*] Input the data to decrypt: ').encode('UTF-8')
    else:
        sys.exit('[-] Wrong type! Terminated.')
    # USER INPUT SECRET KEY
    aes_key = input('[*] Enter security key: ')
    return data, aes_key, file_name, type_of_data

if __name__=='__main__':
    data, aes_key, file_name, type_of_data = user_input()
    try:
        cipher = AESCipher(aes_key).decrypt(data)
    except:
        sys.exit('[-] Wrong Key! String/File not decrypted')
    print('========== RESULT ==========')
    if 'f' in type_of_data:
        os.remove(file_name)
        file_name = file_name.replace('.aes', '')
        f = open(file_name, 'wb')
        f.write(cipher)
        print(f'[+] Encrypted data save in {os.getcwd()}\\{file_name}')
    elif 's' in type_of_data:
        print(f'[+] Encrypted Data: {cipher}')
