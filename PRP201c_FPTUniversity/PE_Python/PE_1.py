import re

def lenCheck(password):
    if len(password) < 6:
        return False
    elif len(password) > 12:
        return False
    return True

def checkChar(password):
    try:
        re.search(r'[a-z]{1,}', password).group(0)
        re.search(r'[A-Z]{1,}', password).group(0)
        re.search(r'[0-9]{1,}', password).group(0)
        re.search(r'[$#@]{1,}', password).group(0)
        return True
    except:
        return False

def user_input():
    valid_password = ''
    uinput = input('Enter your password: ')
    if ',' in uinput:
        listPassword = uinput.split(',')
        for i in range(0, len(listPassword)):
            if lenCheck(listPassword[i]) and checkChar(listPassword[i]):
                if i == len(listPassword):
                    valid_password += f'{listPassword[i]}'
                else:
                    valid_password += f'{listPassword[i]},'
        valid_password = re.sub('[,]{1,}$', '', valid_password)
        return valid_password
    elif lenCheck(uinput) and checkChar(uinput):
        valid_password += uinput
    valid_password = re.sub('[,]{1,}$', '', valid_password)
    return valid_password

if __name__ == '__main__':
    valid_password = user_input()
    if len(valid_password) == 0:
        exit('[-] There is no valid passowrd')
    print(f'[+] Valid passwords: {valid_password}')
