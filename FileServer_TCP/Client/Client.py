#!/usr/bin/env python3

import socket
import struct
import json


def main():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(("127.0.0.1", 8181))
    tcp_client.sendall(struct.pack("!I", 1))
    res = tcp_client.recv(4096)
    print(struct.unpack_from("!I", res)[0])
    res = tcp_client.recv(4096)
    dados = json.loads(res.decode())
    print(dados)
    tcp_client.close()


if(__name__ == "__main__"):
    main()
