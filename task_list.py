import os
from threading import Thread
import threading
from queue import Queue
from time import sleep

USERNAME = "administrator"
PASSWORD = "111111"


def services(ip_queue: Queue, file_queue: Queue):
    while True:
        ip = ip_queue.get()
        if ip == "0" or ip == "":
            ip_queue.put("0")
            break
        f = os.popen("tasklist /s {} /u {} /p {} /v 2>&1".format(ip, USERNAME, PASSWORD))
        # f = os.popen("dir".format(ip))
        outer = f.readlines()
        content = 'IP:{}\n'.format(ip)
        for line in outer:
            content = content + line
        file_queue.put(content)


def file_read():
    with open('test.txt', 'r', encoding='utf-8') as f:
        content = list(f.read().split('\n'))
    return content


def put_queue(f, ip_queue: Queue):
    for ip in f:
        ip_queue.put(ip)
    ip_queue.put("0")


def write_file(file_queue: Queue):
    with open(r'result.txt', 'a') as f:
        while True:
            content = file_queue.get()
            if content == "0":
                break
            f.writelines(content + "\n")


if __name__ == '__main__':
    # pass
    q = Queue(maxsize=300)
    qw = Queue(maxsize=100)
    a = file_read()
    rt1 = Thread(name="Threading-rt1", target=put_queue, args=(a, q))
    wt1 = Thread(name="Threading-Wt1", target=write_file, args=(qw,))
    t = []
    rt1.start()
    wt1.start()
    sleep(1)
    for i in range(20):
        t.append("t{}".format(i))
        t[i] = Thread(name="Threading-{}".format(t[i]), target=services, args=(q, qw))
        t[i].start()
        sleep(0.01)
    while True:
        sleep(1)
        a = len(threading.enumerate())
        if a == 2:
            qw.put("0")
            break
