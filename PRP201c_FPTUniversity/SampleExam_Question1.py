def intCheck(input):
    try:
        int(input)
        return True
    except:
        return False

if __name__=='__main__':
    array = []
    while True:
        preInput = input("[*] Enter a number: ")
        if 'done' in str(preInput):
            exit(f'===== Result =====\n- Num count: {len(array)}\n- Max: {sum(array)}')
        if intCheck(preInput):
            array.append(int(preInput))
        else:
            print('[-] Could not input the string/float type.')