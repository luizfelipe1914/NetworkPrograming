#!/usr/bin/env python3

import socket 

def main():
    host_port = ("0.0.0.0", 8080)
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind(host_port)
    while True:
        data, client = soquete.recvfrom(1024)
        print(f"{client[0]} enviou {data.decode()}")
        soquete.sendto(data, client)
    soquete.close()

if(__name__ == "__main__"):
    main()
