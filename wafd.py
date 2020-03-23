import socket
import concurrent.futures


def connHTTP(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
        s_tcp2.connect(('192.168.17.150', 80))
        s_tcp2.sendall(data)
        data2 = s_tcp2.recv(1024)
        return data2


def initWAF():
    print("***** Web Application Firewall v1.0 *****")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp1:
        s_tcp1.bind(('192.168.17.149', 80))
        s_tcp1.listen(10)

        while True:
            conn, addr = s_tcp1.accept()
            with conn:
                data = conn.recv(1024)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    f1 = executor.submit(connHTTP, data)
                    conn.send(f1.result())


if __name__ == '__main__':
    initWAF()
