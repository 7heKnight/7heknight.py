# Author: 7heKnight
# Tested in Windows 10 20H2 | Python: 3.9.0
# The Code following these structures.
#   netsh wlan show profile
#   netsh wlan show profile <Interface_Name> key=clear
import subprocess
import ctypes
import time
import sys
import os
import re

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def readFile():
    if os.path.isfile(os.getcwd() + r'\' + sys.argv[0] + '.txt'):
        f = open(sys.argv[0] + '.txt', 'r')
        listPassword = f.read().split('\n')
        f.close()
    elif os.path.isfile(sys.argv[0] + '.txt'):
        f = open(sys.argv[0] + '.txt', 'r')
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
    for i in re.findall(r'All User Profile.*', subprocess.check_output(['netsh', 'wlan', 'show', 'profile'], encoding='utf-8')):
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
        beforePassword = re.search(r'Key Content.*', subprocess.check_output(['netsh', 'wlan', 'show', 'profile', interfaceName, 'key=clear'], encoding='utf-8')).group(0)
        password = beforePassword.split(': ')[1]
        return interfaceName, password
    except:
        return '[-] "' + interfaceName + '" not found.', "[-] Password not found."

if __name__=='__main__':
    start = time.time()
    if isAdmin():
        if len(sys.argv) == 1:
            argvLen_1()
        elif len(sys.argv) == 2:
            if sys.argv[1] == '-h':
                print('\nThe code will list all the password of wifi connection\n')
                print('Usage:\n')
                print('\t[*] Get all Interface_name and Password: python ' + sys.argv[0])
                print('\t[*] Get Password from Interface_name: python ' + sys.argv[0] + ' <Interface_name>')
            else:
                interface, password = argvLen_2(sys.argv[1])
                print('\n--- Result ---\n')
                print("Interface: " + interface)
                print("Password:  " + password)
        else:
            print('[-] You should put interface name in "Double Quotes".')
            time.sleep(0.1)  # 0.1 sec
            exit('[-] Argument out of range.')
    else:
        exit('\n[-] Access Denied. You should run as administrator.')
    print('---------------------------------------------------------------------------')
    end = time.time()
    time.sleep(0.0001)
    exit('The program processed in ' + str(end-start) + ' second')
