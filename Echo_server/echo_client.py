#!/usr/bin/env python3

import socket

def main():
    ip_server = input("IP DO SERVIDOR: ")
    server_port = int(input("Porta do servidor: "))
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input("Mensagem: ").encode()
        soquete.sendto(msg, (ip_server, server_port))
        res, server = soquete.recvfrom(1024)
        print(f"Servidor respondeu: {res.decode()}")
    soquete.close()

if(__name__ == "__main__"):
    main()
