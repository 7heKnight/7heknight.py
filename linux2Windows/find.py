from re import search, IGNORECASE, sub, findall
from optparse import OptionParser
from os import walk, path, getcwd
from platform import system
from time import sleep

# Tested on Windows 11 Enterprise Insider Preview v22xxx.xxxx


def options():
    parser = OptionParser('Syntax: Find <-d Directory> <-n File\'s_Name> <-f File\'s_Type>')
    parser.add_option('-d', help=r'Directory.')
    parser.add_option('-f', help=r'File type going to find.')
    parser.add_option('-n', help=r'Name of file going to find.')
    parser.add_option('--content', help=r'Reading and finding the matched content (This option might take long time).')
    (option, argv) = parser.parse_args()
    if not option.f and not option.n and not option.content:
        parser.error('[-] Missing file name, file type and content.')
    return option


# If crashed, means content not found. So no need the variable
def content_finder(file, content):
    with open(file, 'r') as f:
        try:
            search(content, f.read(), IGNORECASE).group(0)
            return True
        except:
            return False


# The main finding function
def find(directory, file_type, file_name, content):
    counter = 0
    if not file_name:
        file_name = '.*'
    if not file_type:
        file_type = '.*'
    if not directory:
        directory = getcwd()
    if '../' in directory or '..\\' in directory or '/..' in directory or '\\..' in directory:
        removable_path = findall(r'\.{2}', directory)
        directory = getcwd()
        for time_to_remove_path in range(len(removable_path)):
            if system() == 'Windows':
                directory = sub(r'\\{1,2}\w+?\\?$', '', directory)
            else:
                directory = sub(r'/{1,2}\w+?/?$', '', directory)
    try:
        for root, dirs, file in walk(directory, topdown=True):
            for name in file:
                try:
                    current_working_dir = path.join(root, name)
                    search(file_name + r'.*' + file_type + r'$', current_working_dir, IGNORECASE).group(0)
                    if content:
                        if content_finder(current_working_dir, content):
                            print(current_working_dir)
                            counter += 1
                    else:
                        print(current_working_dir)
                        counter += 1
                except:
                    pass
    except KeyboardInterrupt:
        exit('[-] Terminated.')
    return counter


if __name__ == '__main__':
    opt = options()
    if opt.content:
        print(f'\n[*] Searching with content: "{opt.content}"\n')
    else:
        print('[*] Searching with none content...\n')

    result = find(opt.d, opt.f, opt.n, opt.content)
    if result == 0:
        from sys import exit
        exit('[-] No result found.')
    print('----------------------------------')
    sleep(0.000000000001)
    print(f'[+] Program executed successfully with {result} results.')
    from sys import exit
    exit(0)
