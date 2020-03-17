import socket
# import threading


def connHTTP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
        s_tcp2.connect(('192.168.0.6', 8080))
        print('Connected with HTTP')
        s_tcp2.sendall(data)
        data2 = s_tcp2.recv(1024)
        # socket_tcp.sendall(data2)
        print(data2)
        return


print("Web Application Firewall v1.0")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
    socket_tcp.bind(('192.168.17.149', 80))
    socket_tcp.listen()
    conn, addr = socket_tcp.accept()
    with conn:
        # print('Connected by: ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # t1 = threading.Thread(target=connHTTP)
            # t1.start()
            # t1.join()
            print(data)
