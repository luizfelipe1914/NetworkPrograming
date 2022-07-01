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



def send_length(con, length):
    try:
        con.sendall(struct.pack("!h", length))
    except Exception as exc:
        print(exc)
        
def file_exists(file):
    files = json.loads(list_files)
    if(files.get(file)):
        return True
    return False
      
def send_file(con, file, initial, finish):
    length = json.loads(list_files)[file]
    if(finish > length or initial > length):
        con.send(struct.pack("!h", 4))
    else:        
        if(finish == 0):
            try:
                with open(file, "rb") as f:
                    if(initial == 0):
                        con.send(struct.pack("!I", len(f)))
                    else:
                        con.send(struct.pack("!I", len(f) - initial))
                    readed = f.read(initial)
                    while(len(readed) < len(f)):
                        r = f.read(4096)
                        con.send(r)
                        readed+=r
                    f.close()
            except Exception as exc:
                print(exc)
        else:
            to_read = finish - initial
            con.send(struct.pack("!I", to_read))
            try:
                with open(file, "rb") as f:
                    readed = f.read(initial)
                    while(len(readed) < finish):
                        r = f.read(4096)
                        con.send(r)
                        readed+=r
                    f.close()
            except Exception as exc:
                print(exc)


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
            res = con.recv(2)
            if(not res):
                break
            else:
                con.send(struct.pack("!h", 1))
                print(f'O cliente {client[0]} enviou {struct.unpack("!I", res)[0]}')
                command = struct.unpack("!h", res)[0]
                if(command == 1):
                    print(f"O cliente {client[0]} solicitou a listagem dos arquivos")
                    send_length(con, len(list_files()))
                    send_list_files(con, list_files())
                elif(res == 2):
                    data = con.recv(4)
                    if(not data):
                        break
                    else:
                        con.send(struct.pack("!h", 1))
                        len_file = struct.unpack("!I", data)[0]
                        name_file = con.recv(len_file)
                        if(not name_file):
                            break
                        else:
                            if(file_exists(name_file.decode("UTF-8"))):
                                while(len(name_file) < len_file):
                                    name_file+=con.recv(len_file)
                                data = con.recv(16)
                                if(not data):
                                    break
                                else:
                                    con.send(struct.pack("!h", 1))
                                    inicio, fim = struct.unpack("!QQ", data)
                                    send_file(con, name_file, inicio, fim)
                            else:
                                con.send(struct.pack("!h", 3)) 
                    
    tcp.close()


if(__name__ == "__main__"):
    main()
