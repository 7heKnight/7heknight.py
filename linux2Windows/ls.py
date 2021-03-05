import os

ls = r''
lsdir = r''
for root, dir, f in os.walk('.'):
    for i in f:
        ls+='"'+i+'"     '
    for i in dir:
        lsdir += '"'+i + '"     '
    print('[+] List dir: ' + lsdir)
    print('[+] List FIles: '+ls)
    break
