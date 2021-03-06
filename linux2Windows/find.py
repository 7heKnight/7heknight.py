from sys import exit
import optparse
import time
import os
import re

def options():
    parser = optparse.OptionParser('Syntax: Find <-d Directory> <-n File\'s_Name> <-f File\'s_Type>')
    parser.add_option('-d', help=r'Directory.')
    parser.add_option('-f', help=r'File type going to find.')
    parser.add_option('-n', help=r'Name of file going to find.')
    parser.add_option('--content', help=r'Reading and finding the matched content (This option might take long time).')
    (option, argv) = parser.parse_args()
    if option.f == None and option.n == None and option.content == None:
        parser.error('[-] Missing file name and file type.')
    return option

def contentFinder(dir, content):
    with open(dir, 'r') as f:
        if content in f.read():
            return True
        return False

def find(directory, fileType, fileName, content):
    listResult = []
    if fileName == None:
       fileName = r'.*'
    if fileType == None:
        fileType = r'.*'
    if directory == None:
        directory = os.getcwd()
    try:
        for root, dir, file in os.walk(directory, topdown=True):
            for name in file:
                try:
                    currentWorkingDir = os.path.join(root, name)
                    try:
                        re.search(fileName + '.*[.]{1}' + fileType + '$', currentWorkingDir, re.I).group(0)
                        if content != None:
                            if contentFinder(currentWorkingDir, content):
                                print(currentWorkingDir)
                                listResult.append(currentWorkingDir)
                        else:
                            print(currentWorkingDir)
                            listResult.append(currentWorkingDir)
                    except:
                        pass

                except KeyboardInterrupt:
                    exit('[-] Terminated.')
    except KeyboardInterrupt:
        exit('[-] Terminated.')
    return listResult

if __name__=='__main__':
    opt = options()
    if opt.content != None:
        print(f'\n[*] Searching with content: "{opt.content}"\n')
    else:
        print('[*] Searching with none content...\n')

    result = find(opt.d, opt.f, opt.n, opt.content)
    if not result:
        exit('[-] No result found.')
    print('----------------------------------')
    time.sleep(0.000000000001)
    exit('[+] Program executed successfully.')

# Tested on Windows 10 Professional
# os.getcwd()
# find -d C:\ -f pdf
# pyinstaller --onefile sys.argv[0]
# the execution file into C:\Windows\System32
