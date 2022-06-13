#!/usr/bin/env python3

import socket
import struct

#def main():
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_port = ("0.0.0.0", 6969)
server_socket.bind(host_port)
data, client = server_socket.recvfrom(1024)
print(f"O cliente {client[0]}, solicitou o arquivo {data.decode()}")
while(True):
    with open(f"{data.decode()}", "rb") as file:
        to_read = len(file.read())
        size = to_read
        readed = 0
        server_socket.sendto(struct.pack("!I", size), client)
        while (to_read >= readed):
            if(to_read >= 512):
                buffer= file.read(512)
                server_socket.sendto(buffer, client)
                to_read -= len(buffer)
                readed+= len(buffer)
            #    print(f"{readed/size}% do arquivo enviados ao cliente...")
            else:
                buffer= file.read(to_read)
                server_socket.sendto(buffer, client)
                to_read -= len(buffer)
                readed+= len(buffer)
            #    print(f"{readed/size}% do arquivo enviados ao cliente...")
        file.close()
        
            

#if("__name__" == "__main__"):
#    main()
