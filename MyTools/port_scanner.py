from sys import exit
import threading
import argparse
import socket
import re


def __option_parser():
    parser = argparse.ArgumentParser(description='This Is port scanner test.')
    parser.add_argument('-p', nargs='?', dest='ports', help='Comma-Seperated port list. E.g: 22,80,443,1-10 ...')
    parser.add_argument('--host', nargs='?', dest='hostname', help='Host of target.')
    options = vars(parser.parse_args())

    if not options['hostname']:
        parser.error('[-] Hostname is required!')
    if not options['ports']:
        parser.error('[-] Port is required!')

    return options['hostname'], options['ports']


def __get_port_list(port_arguments) -> list:
    port_list = port_arguments.split(',')
    final_list = []
    for p in port_list:
        if '-' in p:
            get_range = p.split('-')
            for port in range(int(get_range[0]), int(get_range[1])):
                final_list.append(str(port))
        else:
            final_list.append(p)
    final_list = list(dict.fromkeys(final_list))
    return final_list


def __get_ip_from_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        print(ip_address)
        return ip_address
    except OSError:
        exit(f'[-] Cannot resolve {hostname}: Unknown host!')


def __check_hostname(hostname):
    hostname = re.sub(r'^.+?://', '', hostname)
    hostname = re.search(r'^([\w.]+)/?', hostname)
    if not hostname:
        from sys import exit
        exit('[-] Hostname has wrong format!')
    return hostname.group(1)


def __port_scan(result_list, target, target_port: int):
    try:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn_socket.connect((target, target_port))
            conn_socket.send(b'Banner query\r\n')
            result_list.append(f'   [+] {target_port}/TCP open')
        except OSError:
            pass
        finally:
            conn_socket.close()
    except KeyboardInterrupt:
        exit('[-] Keyboard interruption: Terminated!')


def __multi_scan(result_list, target_host, target_port: int):
    t = threading.Thread(target=__port_scan, args=(result_list, target_host, target_port))
    t.start()


if __name__ == '__main__':
    result = []
    host, list_ports = __option_parser()
    ports = __get_port_list(list_ports)
    print(f'[*] Scan result for {host}:')
    for port in ports:
        __multi_scan(result, host, int(port))
    for i in result:
        print(i)
    print('----------------------------------\n'
          'Program executed successfully')
    exit(0)
