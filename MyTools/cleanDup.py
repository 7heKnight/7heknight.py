# The Code will hash the data of file and put it into an array, and them compare with others file, if exist, it will remove that file. It will make a file(.log) in the
# same folder
# Not recommended using it in root directory
# Maked and tested on Windows 10 pro 20H2 | Python Version: 3.9.0
# How To Use: python sys.argv[0] <Directory>. E.g: python cleanDup.py C:\Users\User_name\Desktop

import hashlib
import time
import sys
import os


def check_directory(directories):
    hash_list = []
    counter = 0
    scanned_counter = 0
    log = open(sys.argv[0] + '.log', 'a+', encoding='UTF-8')
    for root, dirs, files in os.walk(directories, topdown=True):
        is_scanned = False
        for name in files:
            try:
                if not is_scanned:
                    is_scanned = True
                    print(f'\n[+] Scanning the directory: {root}\n')
                f = os.path.join(root, name)
                ff = open(f, 'rb')
                h = make_hash(ff.read())
                ff.close()
                scanned_counter += 1
                if not os.path.isdir(f):
                    if h not in hash_list:
                        hash_list.append(h)
                    else:
                        counter += 1
                        log.write('\n'+str(counter)+'. ' + root + '\\' + name)
                        print('[-] Removed ' + root + '\\' + name)
                        os.remove(f)
            except KeyboardInterrupt:
                scanned_counter += 1
                print('[!] Could not scan the file: ' + root + '\\' + name)
    log.write('\n')
    log.close()
    return counter, scanned_counter


def make_hash(files):
    return hashlib.sha1(files).hexdigest()


if __name__ == '__main__':
    first = time.time()
    directory = sys.argv[1]
    if os.path.isdir(directory):
        count, cS = check_directory(directory)
        print('\n[+] Scanned ' + str(cS) + ' files')
        if count == 0:
            print('\n[*] No files duplicated')
            print('\n[-] Terminate')
            exit('The program processed in ' + str(time.time() - first) + ' sec')
        else:
            print('\n[-] Removed ' + str(count) + ' duplicated files')
            print('[-] Terminate')
            exit('The program processed in ' + str(time.time() - first) + ' sec')
    elif os.path.isfile(directory):
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        print('\n[-] Terminated. Application can not scan the path')
        exit('The program processed in ' + str(time.time() - first) + ' sec')
    else:
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        print('\n[-] Directory not found. Terminated')
        exit('The program processed in ' + str(time.time() - first) + ' sec')
