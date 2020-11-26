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
    count = 0
    line = 0
    path = pathlib.Path(fileDir)
    pathName = str(pathlib.Path(fileDir)).strip(str(pathlib.Path(fileDir).name))
    f = open(fileDir, 'r', encoding='UTF-8')
    for i in f:
        line += 1
        r = i.split('\n')[0]
        keyParser = i.replace('\n', '')
        keyParser = keyParser.replace(' ', '')
        keyParser = keyParser.split('|')
        try:
            if '|' not in r :
                print('[-] Removed the wrong format line: ' + r + '_$') # $ mean end of string
            elif not keyParser[0] == r'' and not keyParser[1] == r'':
                result = re.sub(r'^[0-9\-#./: ) ]{1,5}', '', r)  # 1-Question
                result = re.sub(r'\|[ ]{0,2}[(0-9) ]{0,5}', '| ', result)
                result = re.sub(r'\w{1,5}[=]{1,3}\d{0,10}[ \t]{1,10}[0-9()]{0,9}[ \t]{0,3}', '', result)  # Q1=123[space or tab](123-456)[space or tab]
                result = re.sub(r'[a-eA-E0-9]{1,3}[./]{1,99}[ \t]{1,99}', '', result)  # abc[. or /][space or tab]
                result = re.sub(r'[\t]{1,9}', '', result)  # if equal or more 1 tab, it will remove
                result = re.sub(r'[0-9\-\[\]]{2,99}[ ][a-zA-Z0-9]{1,5}]', '', result)  # [100] T
                result = re.sub(r'[0-9\-\[\]]{2,99}[ ]', '', result)  # [100]
                result = re.sub(r'[ ]{2,99}', ' ', result)  # more than 2 space will place to 1 space
                result = result.replace('�','')
                result = result.replace('*','')
                result = result.replace(' .','.')
                if result in listQA:
                    count += 1
                else:
                    listQA.append(str(result))
            else:
                print('[-] Removed the wrong format line: ' + r + '_$')
        except:
            pass
    f.close()
    print('\n[*] Original file has ' + str(line) + ' lines\n')
    print('[-] Removed ' + str(count) + ' duplicated lines')
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
    f = open(path + name.split('.')[0] + '_copied.' + name.split('.')[1], 'w', encoding='utf-8')
    count = 0
    for i in listQA:
        count+=1
        try:
            f.write(i+'\n')
        except:
            pass
    f.close()
    time.sleep(0.0001)
    exit('\n[+] Copied ' + str(count) + ' lines to created file: ' + path + name.split('.')[0] + '_copied.' + name.split('.')[1])
