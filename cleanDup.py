#The Code will hash the data of file and put it into an array, and them compare with others file, if exist, it will remove that file. It will make a file(.log) in the
# same folder
#Not recommended using it in root directory
#Maked and tested on Windows 10 pro 20H2 | Python Version: 3.9.0
#How To Use: python sys.argv[0] <Directory>. E.g: python cleanDup.py C:\Users\User_name\Desktop

import hashlib
import time
import sys
import os

def openAndCheckDir(dir):
    listHash = []
    count = 0
    countScan = 0
    log = open(sys.argv[0] + '.log', 'a+')
    for root, dirs, files in os.walk(dir, topdown=True):
        isScanning = False
        for name in files:
            try:
                if isScanning == False:
                    isScanning = True
                    print('\n[+] Scanning the directory: '+ root+'\n')
                f = os.path.join(root, name)
                ff = open(f, 'rb')
                h = hashMake(ff.read())
                ff.close()
                countScan += 1
                if not os.path.isdir(f):
                    if h not in listHash:
                        listHash.append(h)
                    else:
                        count += 1
                        log.write('\n'+str(count)+'. ' + root + '\\' + name)
                        print('[-] Removed ' + root + '\\' + name)
                        os.remove(f)
            except:
                countScan += 1
                print('[-] Could not scan the file: ' + root + '\\' + name)
    log.write('\n')
    log.close()
    return count, countScan

def hashMake(Files):
    string = hashlib.sha1(Files).hexdigest()
    return string

if __name__=='__main__':
    first = time.clock()
    dir = sys.argv[1]
    if os.path.isdir(dir):
        count, cS = openAndCheckDir(dir)
        print('\n[+] Scanned ' + str(cS) + ' files')
        if count == 0:
            print('\n[*] No files duplicated')
            print('\n[-] Teminate')
            exit('The program processed in ' + str(time.clock() - first) + ' sec')
        else:
            print('\n[-] Removed ' + str(count) + ' duplicated files')
            print('[-] Teminate')
            exit('The program processed in ' + str(time.clock() - first) + ' sec')
    elif os.path.isfile(dir):
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        print('\n[-] Teminated. Application can not scan the path')
        exit('The program processed in ' + str(time.clock() - first) + ' sec')
    else:
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        print('\n[-] Directory not found. Terminated')
        exit('The program processed in ' + str(time.clock() - first) + ' sec')
