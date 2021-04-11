from subprocess import call, check_output
import optparse
import re

def parserAgrs():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter the interfacename to change. use '-h' to get more information.")
    parser.add_option("-m", '--mac', dest="newMAC", help="Enter the new MAC to change. use '-h' to get more information.")
    (options, agrs) = parser.parse_args()
    if not options.interface:
        parser.error("[-] You need entering the interface")
    elif not options.newMAC:
        parser.error("[-] You need entering the interface")
    return options

def checkInterface(interface):
    try:
        output = check_output(["ifconfig", interface])
        MAC = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', output)
        if not MAC:
            print("[-] The interface does not have accept the MAC address, please try with another interface.")
            exit(0)
        return MAC.group(0)
    except:
        print('[-] Interface name not found. Teminating...')
        exit(0)

def changeMAC(interface, newMAC):
    print('[+] Turning down the interface')
    call(["ifconfig", interface, "down"])
    print('[+] Done\n[+] Chaging the MAC of '+interface)
    call(["ifconfig", interface, "hw", "ether", newMAC])
    print('[+] Changed successfully. Now your MAC of ' + interface + " is " + newMAC + ".")
    print('[+] Turning up the interface')
    call(["ifconfig", interface, "up"])
    print('[+] Done.')

if __name__ == '__main__':
    print("[+] Executing...")
    option = parserAgrs()
    mac = checkInterface(option.interface)
    print("[+] found the "+option.interface + 'with the MAC: ' + mac)
    changeMAC(option.interface, option.newMAC )