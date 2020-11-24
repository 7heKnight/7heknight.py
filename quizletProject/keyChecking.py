import pathlib
import sys
import re
import os

def parser(fileDir):
    answer = []
    path = pathlib.Path(fileDir)
    pathName = str(pathlib.Path(fileDir)).strip(str(pathlib.Path(fileDir).name))
    f = open(fileDir, 'r', encoding="utf-8")
    for i in f:
        result = re.sub(r'\w{1,5}[=]{1,3}\d{0,10}[ ]{0,10}', '', i.split('\n')[0])
        afterResult = re.sub(r'[a-eA-E]{1}[./]{1,99}[ ]{0,99}', '', result)
        answer.append(afterResult)
    f.close()
    return answer, pathName, str(path.name)

if __name__=='__main__':
    a = []
    q = []
    fileDir = None
    path = 0
    name = 0
    if len(sys.argv) == 2:
        fileDir = sys.argv[1]
        if os.path.isfile(fileDir):
            a, path, name = parser(fileDir)
        else:
            exit('[-] You need input the Path + File_Name')
    elif len(sys.argv) == 1:
        fileDir = input('[*] Enter File Direction: ')
        if os.path.isfile(fileDir):
            a, path, name = parser(fileDir)
        else:
            exit('[-] You need input the Path + File_Name')
    else:
        exit('[-] Terminated')
    f = open(path + 'Copied_' + name, 'w')
    for i in a:
        try:
            f.write(i+'\n')
        except:
            pass
    f.close()
