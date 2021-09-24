from os import walk

for root, directories, files in walk('.'):
    if directories != []:
        print('\n[+] List Directory:')
        for i in directories:
            print(i, end='\t')
            print('\n')
    if files != []:
        print('\n[+] List Files:')
        for i in files:
            print(i, end='    ')
    if files == [] and directories == []:
        print('[-] There is no file or directory here.')
    print()
    break
