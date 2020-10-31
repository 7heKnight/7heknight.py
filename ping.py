import subprocess
import optparse
import platform
import re

def optParser():
    parser = optparse.OptionParser('Usage: python ping.py -n <Times to ping> -d <IPv4|Domain>')
    parser.add_option('-n', dest='TimesToPing', help='Enter times to ping')
    parser.add_option('-d', '--domain', dest='Domain', help='Enter IP version 4 or Domain name')
    (options, agrs) = parser.parse_args()
    if not options.TimesToPing:
        parser.error("[-] You should input the option '-n' for the times of pingging. Use '-h' to get more help.")
    elif not options.Domain:
        parser.error("[-] You should input the IP or Domain_name with the option '-d'. Use '-h' to get more help.")
    return options

def ifWindows(domain):
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

if __name__ == '__main__':
    options = optParser()
    os = platform.system().lower()
    if os == 'windows':
        for i in range(1, int(options.TimesToPing)):
            print(ifWindows(options.Domain))
    elif os == 'linux':
        subprocess.call(['ping', '-c', options.TimesToPing, options.Domain])