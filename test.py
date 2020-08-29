import os
import socket
def services(ips):
    for ip in ips:
        f=os.popen("tasklist /s {} /u administrator /p 111111 /v".format(ip))
        a=f.readlines()
        for i in a:
            print(i,end='')
if __name__ == '__main__':
    services(['192.168.202.134'])