import time
import os
lib = ['PyCryptodome']
for i in lib:
    print(f'\n[*] Installing {i}...')
    os.system(f'pip install {i}')