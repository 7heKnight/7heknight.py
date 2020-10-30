import itertools
import requests
import optparse
import re

def aguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", dest="URL", help="The URL of the website. E.g: -u http://127.0.0.1/")
    parser.add_option("-s", "--subdirectory", dest="Subdirectory", help="The sub-directory you going to check. E.g: -s ABCDEF123")
    # parser.add_option("-h", "--help", help="Example given: python filename.py -u http://127.0,0,1/ -sD ABCDE123")
    (options, arguments) = parser.parse_args()
    if not options.URL:
        parser.error("\n[-] You need input the URL. <yourscript> -h or <yourscript> --help to find option")
    elif not options.Subdirectory:
        parser.error("\n[-] You need input the URL. <yourscript> -h or <yourscript> --help to find option")
    return options

def dirCheck(directory):
    regexDir = re.search(r"https://.*|http://.*", directory)
    if not regexDir:
        print(f"You need to start with http:// or https://")
        exit(0)
    try:
        openDir = requests.get(directory)
        directory = openDir.url
        if openDir.status_code:
            return directory
    except:
        print("Error with the directory.")
        exit(0)

if __name__=="__main__":
    options = aguments()
    print("[+] Checking...\n")
    dir = dirCheck(options.URL)
    dir = str(dir)
    sub_dir = options.Subdirectory.upper()
    combination = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in sub_dir)))
    try:
        for c in combination:
            r = requests.get(dir + c)
            if (r.status_code == requests.codes.ok):
                print("[+] " + dir + c)
    except:

        print("[-] Teminated. Good bye!")
        exit(0)
    print("\n[-] Done, exiting")

# https://pastebin.com/
# HEJXMAJW