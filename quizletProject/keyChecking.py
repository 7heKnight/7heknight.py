# This tool created to remove some annoying key like: a. b. c. , a/ b/ c/,....
# Usage: 1. python File.py <FileDirection>
#        2. Python File.py
import pathlib
import sys
import re
import os

def parser(fileDir):
    listQA = []
    path = pathlib.Path(fileDir)
    pathName = str(pathlib.Path(fileDir)).strip(str(pathlib.Path(fileDir).name))
    f = open(fileDir, 'r', encoding='UTF-8')
    for i in f:
        result = re.sub(r'\w{1,5}[=]{1,3}\d{0,10}[ \t]{1,10}', '', i.split('\n')[0])
        afterResult = re.sub(r'[a-eA-E0-9]{1,3}[./]{1,99}[ \t]{1,99}', '', result)
        listQA.append(str(afterResult))
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
    for i in listQA:
        try:
            f.write(i+'\n')
        except:
            pass
    f.close()
