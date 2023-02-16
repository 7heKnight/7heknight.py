from os.path import isfile
from os import remove
from sys import argv, exit
import subprocess

if __name__ == '__main__':
    """
    Requires OpenSSL:
    - https://wiki.openssl.org/index.php/Binaries
    """
    if len(argv) != 2:
        print("Public Key Required!")
        exit(-1)
    try:
        open('tmp_data', 'w').write(f'-----BEGIN RSA PRIVATE KEY-----\n{argv[1]}\n-----END RSA PRIVATE KEY-----\n')
        output = subprocess.getoutput('openssl rsa -in tmp_data -pubout')
        print(output.replace('writing RSA key', ''))
    except:
        pass

    if isfile('tmp_data'):
        remove('tmp_data')
