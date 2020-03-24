import socket
# import concurrent.futures
import threading


def connHTTP(conn, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
        s_tcp2.connect(('192.168.17.150', 80))
        s_tcp2.sendall(data)
        data2 = s_tcp2.recv(1024)
        conn.send(data2)


def initWAF():
    print("***** Web Application Firewall v1.0 *****")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp1:
        s_tcp1.bind(('192.168.17.149', 80))
        s_tcp1.listen()

        while True:
            conn, addr = s_tcp1.accept()
            while True:
                with conn:
                    data = conn.recv(1024)
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #    results = [executor.submit(connHTTP, data)]
                    #    for f in concurrent.futures.as_completed(results):
                    #        print(f.result())
                    #        conn.sendall(f.result())
                    if not data:
                        break
                    thread = threading.Thread(target=connHTTP,
                                              args=(conn, data))
                    thread.start()
                    thread.join()


if __name__ == '__main__':
    initWAF()
