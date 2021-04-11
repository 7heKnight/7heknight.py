import sys
import re

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

def removeUnwantted(file):
    data = []

    if isFile(file):

        lines = open(file, 'r').read().split('\n')
        for line in lines:
            if line == '':
                lines.remove(line)
            else:
                line = re.sub(r'[^a-zA-Z]', '', line)
                data.append(line+'\n')
                print(line)

        fileName, fileType = getFileName(file)
        with open(fileName + '_copy' + fileType, 'w') as f:
            for i in data:
                f.write(i)

    else:
        exit('[-] File not found.')

if __name__ =='__main__':
    if '-h' in sys.argv:
        exit(f'[*] Usage: python {sys.argv[0]} <File>>')
    if not len(sys.argv) == 2:
        exit(f'[-] Usage: python {sys.argv[0]} <File>')
    else:
        removeUnwantted(sys.argv[1])