import urllib.parse
from pymongo import MongoClient
import socket
import threading
import re


def extractURI(data):
    uri = bytearray()
    flag = 0

    for byte in data:
        if byte == 32:
            flag += 1
            continue
        if flag == 1:
            uri.append(byte)
        elif flag == 2:
            break

    return uri.decode('utf-8')


def extractRequestM(data):
    method = bytearray()
    flag = 0

    for byte in data:
        if byte == 32:
            flag += 1
            continue
        if flag == 0:
            method.append(byte)
        elif flag == 1:
            break

    return method.decode('utf-8')


def insertMongoDB(uri, conn, requestM):
    username = urllib.parse.quote_plus('@dm1n')
    password = urllib.parse.quote_plus('Qw3rt&.12345')
    client = MongoClient('mongodb://%s:%s@192.168.17.146' %
                         (username, password))
    db = client['waf']
    collection = db['trama']
    collection.insert_one(
        {'name': 'trama', 'ip': str(conn), 'valor': uri,
         'veredicto': '0', 'tipo': requestM.lower(), 'analizado': 'False'})

    while True:
        doc = collection.find_one({'name': 'trama'})
        if doc['analizado'] == 'True':
            break

    return doc['veredicto']


def connHTTP(conn, data):
    requestM = extractRequestM(data)
    veredicto = '0'

    if requestM == "GET":
        uri = extractURI(data)
        if re.match("/.*\\?.*", uri):
            veredicto = insertMongoDB(uri, conn, requestM)

    if veredicto == '0':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
            s_tcp2.connect(('192.168.17.150', 80))
            s_tcp2.sendall(data)
            data2 = s_tcp2.recv(1024)
            conn.send(data2)
    else:
        print("SQL Injection Atack!")


def initWAF():
    print("***** Web Application Firewall v1.0 *****")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp1:
        s_tcp1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp1.bind(('192.168.17.149', 80))
        s_tcp1.listen()

        while True:
            conn, addr = s_tcp1.accept()
            with conn:
                data = conn.recv(1024)
                thread = threading.Thread(target=connHTTP,
                                          args=(conn, data))
                thread.start()
                thread.join()


# if __name__ == '__main__':
#    initWAF()
