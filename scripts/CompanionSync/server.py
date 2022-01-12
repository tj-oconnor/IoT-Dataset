#!/usr/bin/env python3


"""
grep -ri "192.168"
main/java/edu/fltech/notificationsync/DataSender.java: socket = new Socket("192.168.2.100", 8765);
"""

import socket
import selectors
import json
HOST = "192.168.2.100"
PORT = 8765


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))

s.listen()
while True:
    conn, addr = s.accept()
    with conn:
        data = conn.recv(2048)
        obj = json.loads(data)
        print(data.decode('utf-8'))