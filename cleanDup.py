import hashlib
import sys
import os

def openAndCheckDir(dir):
    listHash = []
    count = 0
    countScan = 0
    log = open(sys.argv[0] + '.log', 'a+')
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            try:
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
                        log.write('\n'+str(count)+'. ' + root + name)
                        print('[-] Removed ' + root + name)
                        os.remove(f)
            except:
                countScan += 1
                print('[-] Could not scan the file: ' + root+name)
    log.write('\n')
    log.close()
    return count, countScan

def hashMake(Files):
    string = hashlib.sha1(Files).hexdigest()
    return string

if __name__=='__main__':
    dir = sys.argv[1]
    if os.path.isdir(dir):
        count, cS = openAndCheckDir(dir)
        print('\n[+] Scanned ' + str(cS) + ' files')
        if count == 0:
            print('\n[*] No files duplicated')
            exit('\n[-] Teminate')
        else:
            print('\n[-] Removed ' + str(count) + ' duplicated files')
            exit('[-] Teminate')
    elif os.path.isfile(dir):
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        exit('\n[-] Teminated. Application can not scan the path')
    else:
        print('\nUsage: ' + sys.argv[0] + ' <Directory>')
        exit('\n[-] Directory not found. Terminated')
