import sys
import os
import re

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f'[-] Could not execute. To use: python {sys.argv[0]} <file_to_parse>')
    FILE_NAME = sys.argv[1]
    if not os.path.isfile(FILE_NAME):
        sys.exit(f'[-] File {FILE_NAME} not found')
    data = open(FILE_NAME, 'r').read()
    paths = re.findall(r'<url><!\[CDATA\[https://www.link.7k/(.+?)/.*]]></url>', data)
    paths.sort()
    if paths == '':
        sys.exit('[-] There is no link found')
    out_file = open('paths.txt', 'w')
    wrote_file = [] # This list is used to double check and remove duplicate string
    count = 0
    for path in paths:
        if path != '/' and not path in wrote_file:
            count +=1
            out_file.write(path+'\n')
            wrote_file.append(path)
    print(f'[+] Wrote {count} paths into: {os.getcwd()}\\paths.txt')
