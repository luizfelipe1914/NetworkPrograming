#!/usr/bin/env python3

import socket
import struct

#def main():
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = input("Qual o IP do servidor: ")
file  = input("Qual arquivo deseja baixar? ")
client_socket.sendto(file.encode(), (server, 6969))
data, server = client_socket.recvfrom(4)
file_size = len(struct.unpack("!I", data))
received  = 0
with open(file, "wb") as file:
    while (file_size >= received):
        if((file_size - received) >= 512):
            data, server = client_socket.recvfrom(512)
            file.write(data)
            received += 512
            print(f"{received/file_size}% do arquivo baixados...")
        else:
            data, server = client_socket.recvfrom((file_size - received))
            file.write(data)
            received += (file_size - received)
            print(f"{received/file_size}% do arquivo baixados...")
    file.close()
client_socket.close()

    
#if("__name__" == "__main__"):
#    main()
