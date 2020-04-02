import urllib.parse
from pymongo import MongoClient
import socket
import threading
import re


def extractParam(data):
    param = data.decode('utf-8').split('\r\n\r\n')
    return param[1]


def extractURI(data):
    uri = data.decode('utf-8').split('\r\n')
    uri = uri[0].split(' ')

    return uri[1]


def extractRequestM(data):
    method = data.decode('utf-8').split('\r\n')
    method = method[0].split(' ')

    return method[0]


def extractAgent(data):
    agent = data.decode('utf-8').split('\r\n')

    return agent[4]


def insertMongoDB(uri, addr, requestM, agent):
    username = urllib.parse.quote_plus('@dm1n')
    password = urllib.parse.quote_plus('Qw3rt&.12345')
    client = MongoClient('mongodb://%s:%s@192.168.17.146' %
                         (username, password))
    db = client['waf']
    collection = db['trama']

    collection.insert_one(
        {'name': 'trama', 'ip': str(addr[0]), 'valor': uri, 'agent': agent,
         'veredicto': '0', 'tipo': requestM.lower(), 'analizado': 'False'})

    while True:
        doc = collection.find_one({'name': 'trama'})
        if doc['analizado'] == 'True':
            break

    collection.delete_one({'name': 'trama'})

    return doc['veredicto']


def connHTTP(conn, addr, data):
    requestM = extractRequestM(data)
    veredicto = '0'

    if requestM == "GET":
        uri = extractURI(data)
        if re.match("/.*\\?.*", uri):
            agent = extractAgent(data)
            veredicto = insertMongoDB(uri, addr, requestM, agent)
    elif requestM == "POST":
        agent = extractAgent(data)
        param = extractParam(data)
        veredicto = insertMongoDB(param, addr, requestM, agent)

    if veredicto == '0':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
            s_tcp2.connect(('192.168.17.158', 80))
            s_tcp2.sendall(data)
            data2 = s_tcp2.recv(1024)
            conn.send(data2)


def initWAF():
    # print("***** Web Application Firewall v1.0 *****")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp1:
        s_tcp1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp1.bind(('192.168.17.149', 80))
        s_tcp1.listen()

        while True:
            conn, addr = s_tcp1.accept()
            with conn:
                data = conn.recv(1024)
                thread = threading.Thread(target=connHTTP,
                                          args=(conn, addr, data))
                thread.start()
                thread.join()
