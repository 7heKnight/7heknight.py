#! /usr/bin/env python3
import random
import string
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit(f'[-] Missing Length for password. E.g: {sys.argv[0]} 10')
    try:
        characters_raw = string.digits + string.ascii_letters
        characters = ''
        if int(sys.argv[1]) > len(characters):
            spawn = int(int(sys.argv[1])/len(characters_raw))
            if len(characters_raw) * spawn - int(sys.argv[1]) < 0:
                spawn += 1
            characters = ''.join(characters+characters_raw for i in range(0,int(spawn)))
        password_length = int(sys.argv[1])
        password = "".join(random.sample(characters, password_length))
        print(f"Gernerated password: {password}")
    except:
        sys.exit('[-] Interger only')
