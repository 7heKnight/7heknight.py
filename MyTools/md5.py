from hashlib import md5
from os.path import isfile
from sys import argv

if __name__=='__main__':
    if len(argv) != 2 or '-h' in argv:
        exit(f'[*] Usage: py {argv[0]} <File>')
    if not isfile(argv[1]):
        exit(f'[-] File "{argv[1]}" not found!')
    print("MD5: " + md5(open(argv[1], 'rb').read()).hexdigest())

