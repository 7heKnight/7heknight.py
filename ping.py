import subprocess
import optparse
import platform
import sys
import re

def optParser():
    parser = optparse.OptionParser('Usage: python ' + sys.argv[0] + ' -n <Times to ping> <IPv4|Domain>')
    parser.add_option('-n', dest='TimesToPing', help='Enter times to ping')
    (options, agrs) = parser.parse_args()
    if not options.TimesToPing:
        parser.error("[-] You should input the option '-n' for the times of pingging. Use '-h' to get more help.")
    return options

def ifWindows(domain):
    try:
        result = subprocess.check_output(['ping', '-n', '1', domain])
        regex = re.search(r"Reply from \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}: bytes=\d{1,3} time=\d{1,3}ms TTL=\d{1,3}", str(result))
        regex1 = re.search(r"Reply from \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}: bytes=\d{1,3} time<\d{1,3}ms TTL=\d{1,3}", str(result))
        if regex:
            return regex.group(0)
        elif regex1:
            return regex1.group(0)
        else:
            print('[-] Pingging time out or ping request could not find the host')
            exit(0)
    except:
        print("[-] The host timeout")
        exit(0)
def ifLinux(domain):
    try:
        result = subprocess.check_output(['ping', '-c', '1', domain])
        regex = re.search(r"\d{1,3} .* \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.*ms", str(result))
        if regex:
            return regex.group(0)
        else:
            print('[-] Pingging time out or ping request could not find the host')
            exit(0)
    except:
        print("[-] The host timeout")
        exit(0)

if __name__ == '__main__':
    options = optParser()
    domain = sys.argv[len(sys.argv)-1]
    os = platform.system().lower()
    if os == 'windows':
        for i in range(1, int(options.TimesToPing)):
            print('[+] '+ifWindows(domain))
    elif os == 'linux':
        for i in range(1, int(options.TimesToPing)):
            print('[+] ' + ifLinux(domain))
