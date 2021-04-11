import sys
import re

ERROR = '[-] File not found!'

def isFile(file):
    try:
        open(file, 'r')
        return True
    except:
        return False

def getFileName(file):
    try:
        name = re.search(r'[/\\]{0,1}(.*)[.]{1}\w{0,4}$', file).group(1)
        fileType = '.' + re.search(r'[/\\]{0,1}.*[.]{1}(\w{1,4})$', file).group(1)
    except:
        name = re.search(r'[/\\]{0,1}(.*)$', file).group(1)
        fileType = ""
    return name, fileType

def convert(rawData):
    converttedList = []
    IPPorts = re.findall("(\d{,3}[.]\d{,3}[.]\d{,3}[.]\d{,3}:\d{1,5})", rawData)
    for i in IPPorts:
        IP = i.split(':')[0]
        Port = i.split(':')[1]
        converttedList.append({'IP': IP, 'Port': Port})
    return converttedList

def newFormat(file):
    data = open(file, 'r').read()
    myFormat = convert(data)
    fileName, fileType = getFileName(file)
    f = open(fileName+'_copy'+fileType,'w')
    f.write(str(myFormat))

if __name__ == '__main__':
    FILE = sys.argv[1]
    if len(sys.argv) == 2:
        if isFile(FILE):
            newFormat(FILE)
        else:
            exit(ERROR)
    else:
        exit(ERROR)