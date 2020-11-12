# Author: 7heKnight
# Tested in Windows 10 20H2 | Python: 3.9.0
# The Code following these structures.
# netsh wlan show profile
# netsh wlan show profile <Interface_Name> key=clear
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

def argvLen_1():
    listInterface = []
    result = re.findall(r".*: .*", subprocess.check_output(['netsh', 'wlan', 'show', 'profile'], shell=True).decode('utf-8'))
    for i in result:
        listInterface.append(str(i).replace('    All User Profile     : ', '')) # Remove the matched string
    for i in listInterface:
        (interface, password) = argvLen_2(i)
        if password == '[-] Password not found.':
            pass
        else:
            print("Interface: " + i)
            print("Password:  " + password)
            print("")

def argvLen_2(interfaceName):
    try:
        interfaceName = interfaceName.replace("\r", '')
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', interfaceName, 'key=clear'], shell=True).decode('utf-8')
        beforePassword = re.search(r'.*Key Content.*:.*', result).group(0)
        password = beforePassword.replace('    Key Content            : ', '')
        return interfaceName, password
    except:
        return '[-] "' + interfaceName + '" not found.', "[-] Password not found."

if __name__=='__main__':
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
                print("Interface: " + interface)
                print("Password: " + password)
        else:
            exit('[-] Argument out of range.')
    else:
        print('[-] You should put interface name in "Double Quotes".')
        time.sleep(0.1) # 0.1 sec
        exit('[-] Access Denied.')
