# This tool created to remove some annoying key like: a. b. c. , a/ b/ c/,....
# Usage: 1. python File.py <FileDirection>
#        2. Python File.py

import pathlib
import time
import sys
import re
import os

def parser(fileDir):
    listQA = []
    path = pathlib.Path(fileDir)
    pathName = str(pathlib.Path(fileDir)).strip(str(pathlib.Path(fileDir).name))
    f = open(fileDir, 'r', encoding='UTF-8')
    for i in f:
        r = i.split('\n')[0]
        keyParser = i.replace('\n', '')
        keyParser = keyParser.replace(' ', '')
        keyParser = keyParser.split('|')
        try:
            if '|' not in r:
                print('[-] Removed the wrong format line: ' + r + '_$')
            elif not keyParser[0] == r'' and not keyParser[1] == r'':
                result = re.sub(r'^[0-9\-#./: ) ]{1,5}', '', r)
                result = re.sub(r'\|[ ]{0,2}[(0-9) ]{0,5}', '| ', result)
                result = re.sub(r'\w{1,5}[=]{1,3}\d{0,10}[ \t]{1,10}[0-9()]{0,9}[ \t]{0,3}', '', result) 
                result = re.sub(r'[a-eA-E0-9]{1,3}[./]{1,99}[ \t]{1,99}', '', result)
                result = re.sub(r'[\t]{1,9}', '', result)
                result = re.sub(r'[0-9\-\[\]]{2,99}[ ][a-zA-Z0-9]{1,5}]', '', result)
                result = re.sub(r'[0-9\-\[\]]{2,99}[ ]', '', result)
                result = re.sub(r'[ ]{2,99}', ' ', result)
                listQA.append(str(result))
            else:
                print('[-] Removed the wrong format line: ' + r + '_$')
        except:
            pass
    f.close()
    return listQA, str(pathName), str(path.name)

if __name__=='__main__':
    listQA = []
    fileDir = None
    path = 0
    name = 0
    if len(sys.argv) == 2:
        fileDir = sys.argv[1]
        if os.path.isfile(fileDir):
            listQA, path, name = parser(fileDir)
        else:
            exit('[-] You need input the Path + File_Name')
    elif len(sys.argv) == 1:
        fileDir = input('[*] Enter File Direction: ')
        if os.path.isfile(fileDir):
            listQA, path, name = parser(fileDir)
        else:
            exit('[-] You need input the Path + File_Name')
    else:
        exit('[-] Terminated')
    f = open(path + 'Copied_' + name, 'w', encoding='UTF-8')

    count = 0
    for i in listQA:
        count+=1
        try:
            f.write(i+'\n')
        except:
            pass
    f.close()
    time.sleep(0.0001)
    exit('\n[+] Copied ' + str(count) + ' lines to created file: ' + path + 'Copied_' + name)
