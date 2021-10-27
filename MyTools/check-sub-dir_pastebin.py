# E.g: 
#   [+] Valid URL: https://pastebin.com/N3f0aqsS (200)
#   [+] Invalid URL: https://pastebin.com/n3f0aqss (404)
#   [*] Usage: python check-sub-dir_pastebin.py <Invalid URL>
from itertools import product
from sys import exit, argv
from re import search
import requests


def get_path(url: str):
    try:
        link = search(r'^http[s]://[^/]+?/', url).group(0)
        path = search(r'[^/]+?$', url).group(0)
        return link, path.upper()
    except:
        print('[-] Could not found path or URL')
        exit(0)


if __name__ == "__main__":
    if len(argv) != 2:
        exit(f'[-] Invalid argument.\n'
             f'\tPlease try: {argv[0]} <URL>')
    print("[+] Checking...")
    url, path = get_path(argv[1])
    list_brute_force = map(''.join, product(* ((char.upper(), char.lower()) for char in path)))
    for bf_path in list_brute_force:
        try:
            respond = requests.get(url + bf_path)
            if respond.ok:
                print(f"[+] Found: {url}{bf_path}")
                exit(0)
        except KeyboardInterrupt:
            exit('[-] Keyboard Interrupted! Terminate.')
    print('[-] Could find valid link.')
