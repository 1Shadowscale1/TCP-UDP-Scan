from queue import Queue
import socket
import time
import urllib.request
import urllib.error
import argparse
import threading


def scntcp(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            s.connect((addr, port))
            print('TCP port opened:', port)
        except:
            pass


def scnudp(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        try:
            s.sendto(b'\x00' * 64, (addr, port))
            d, _ = s.recvfrom(512)
            print("UDP port opened:", str(port))
        except socket.error:
            pass


def getaddr(arg):
    def test():
        try:
            return urllib.request.urlopen('http://google.com/', timeout=10)
        except:
            print("No connection")
    
    if test() is None:
        return
    else:
        try:
            return socket.gethostbyname(arg)
        except:
            print("Unable to allow domain name")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('host_name', type=str)
    parser.add_argument('-f', default=100, type=int, help='Upper border of scanning ports')
    parser.add_argument('-s', default=1, type=int, help='Bottom border of scanning ports')
    parser.add_argument('-udp', action='store_true', help='UDP ports')
    parser.add_argument('-tcp', action='store_true', help='TCP ports')
    args = parser.parse_args()
    if not args.tcp and not args.udp:
        args.tcp = args.udp = True
    addr = getaddr(args.host_name)
    if addr != None:
        print('Starting scan on host: ', addr)
        if args.tcp:
            socket.setdefaulttimeout(1)
            q = Queue()
            start = time.time()
            def thrd():
                while True:
                    port_num = q.get()
                    scntcp(addr, port_num)
                    q.task_done()

            for _ in range(100):
                t = threading.Thread(target=thrd)
                t.daemon = True
                t.start()
            for port in range(args.s, args.f):
                q.put(port)

            q.join()
            print('Time taken for {}'.format(scntcp.__name__), time.time() - start)
        if args.udp:
            socket.setdefaulttimeout(1)
            q = Queue()
            start = time.time()
            def thrd():
                while True:
                    port_num = q.get()
                    scnudp(addr, port_num)
                    q.task_done()

            for _ in range(100):
                t = threading.Thread(target=thrd)
                t.daemon = True
                t.start()
            for port in range(args.s, args.f):
                q.put(port)

            q.join()
            print('Time taken for {}'.format(scnudp.__name__), time.time() - start)