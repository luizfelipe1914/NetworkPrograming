#!/usr/bin/env python3

import socket
import os
import os.path
import struct
import json


def list_files():
    base_dir = f"{os.path.dirname(os.path.abspath(__file__))}{os.path.sep}arquivos"
    files_length = {}
    for file in os.listdir(base_dir):
        if(os.path.isfile(os.path.join(base_dir, file))):
            files_length[file] = os.stat(os.path.join(base_dir, file)).st_size
    return json.dumps(files_length, indent=4, sort_keys=True)


def send_list_files(con, lista):
    con.sendall(bytearray(lista, encoding="utf8"))
    # res = con.recv(4096)
    # return res


def send_length(con, length):
    try:
        con.send(struct.pack("!I", length))
        #res = con.recv(4096)
    except Exception as exc:
        print(exc)
    #return res


def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER = "0.0.0.0"
    PORT = 8181
    try:
        tcp.bind((SERVER, PORT))
        tcp.listen(10)
    except Exception as exc:
        print(exc)
    while True:
        con, client = tcp.accept()
        print(f"{client[0]} conectou")
        while True:
            res = con.recv(4096)
            if(not res):
                break
            else:
                print(f'O cliente {client[0]} enviou {struct.unpack("!I", res)[0]}')
                if(struct.unpack("!I", res)[0] == 1):
                    send_length(con, len(list_files()))
                    send_list_files(con, list_files())
    tcp.close()


if(__name__ == "__main__"):
    main()
