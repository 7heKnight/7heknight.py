# Author: 7heKnight
# Tested in Windows 10 20H2 | Python: 3.9.0
# The Code following these structures.
#   netsh wlan show profile
#   netsh wlan show profile <Interface_Name> key=clear
from subprocess import check_output
from re import search, findall
from os import path, getcwd
from sys import argv, exit
import ctypes

def isAdmin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def readFile():
    listPassword = []
    if path.isfile(getcwd() + '\\' + argv[0] + '.txt'):
        f = open(argv[0] + '.txt', 'r')
        listPassword = f.read().split('\n')
        f.close()
    elif path.isfile(argv[0] + '.txt'):
        f = open(argv[0] + '.txt', 'r')
        listPassword = f.read().split('\n')
        f.close()
    return listPassword

def readPwd():
    try:
        f = open('ListWifiPassword.txt', 'r')
        readFile = f.read()
        f.close()
        readFile = readFile.split('\n')
        readFile.pop()
        return readFile
    except:
        return None

def argvLen_1():
    listPassword = readPwd()
    listInterface = []
    f = open('ListWifiPassword.txt', 'a')
    for i in findall(r'All User Profile.*', check_output(['netsh', 'wlan', 'show', 'profile'], encoding='utf-8')):
        listInterface.append(str(i).split(': ')[1])
    listInterface.pop()
    print('\n--- Result ---\n')
    for i in listInterface:
        (interface, password) = argvLen_2(i)
        if password == '[-] Password not found.':
            pass
        else:
            print("Interface: " + i)
            print("Password:  " + password)
            print("")
            if listPassword == None:
                f.write(password+'\n')
            else:
                if password in listPassword:
                    pass
                else:
                    f.write(password+'\n')
    f.close()

def argvLen_2(interfaceName):
    try:
        beforePassword = search(r'Key Content.*', check_output(['netsh', 'wlan', 'show', 'profile', interfaceName, 'key=clear'], encoding='utf-8')).group(0)
        password = beforePassword.split(': ')[1]
        return interfaceName, password
    except:
        return '[-] "' + interfaceName + '" not found.', "[-] Password not found."

if __name__=='__main__':
    if isAdmin():
        if len(argv) == 1:
            argvLen_1()
        elif len(argv) == 2:
            if argv[1] == '-h':
                print('\nThe code will list all the password of wifi connection\n')
                print('Usage:\n')
                print('\t[*] Get all Interface_name and Password: python ' + argv[0])
                print('\t[*] Get Password from Interface_name: python ' + argv[0] + ' <Interface_name>')
            else:
                interface, password = argvLen_2(argv[1])
                print('\n--- Result ---\n')
                print("Interface: " + interface)
                print("Password:  " + password)
        else:
            print('[-] You should put interface name in "Double Quotes".')
            exit('[-] Argument out of range.')
    else:
        exit('\n[-] Access Denied. You should run as administrator.')
    print('---------------------------------------------------------------------------')
    exit('[+] Program executed done!')
