import socket
import threading
import signal


def connHTTP(s_tcp1, **param):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
        s_tcp2.connect(('192.168.17.150', 8080))
        s_tcp2.sendall(param['data'])
        data2 = s_tcp2.recv(1024)
        s_tcp1.sendall(data2)
        print(data2)
        return


def initWAF():
    print("Web Application Firewall v1.0")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp1:
        s_tcp1.bind(('192.168.17.149', 80))
        s_tcp1.listen(5)

        while True:
            conn, addr = s_tcp1.accept()
            data = conn.recv(1024)
            if not data:
                break
            t1 = threading.Thread(target=connHTTP,
                                  args=(s_tcp1, ),
                                  kwargs={'data': data})
            t1.start()
            t1.join()


if __name__ == '__main__':
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    initWAF()
