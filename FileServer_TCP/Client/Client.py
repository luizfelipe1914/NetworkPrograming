#!/usr/bin/env python3

import socket
import struct
import json


def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor = input("Informe o endereço IPv4 ou domínio do servidor: ")
    PORT = 8181
    try:
        tcp.connect((servidor, PORT))
    except Exception as exc:
        print(exc)
    option = 0
    while(option != 3):
        print("-=-"*10,"MENU","-=-"*10)
        print("[1] Listar arquivos no servidor")
        print("[2] Baixar arquivo do servidor")
        print("[3] Sair")
        try:
            option = int(input())
        except Exception as exc:
            print(exc)
        if(option == 1):
            print(f"Você escolheu listar os arquivos do servidor: ")
            tcp.send(struct.pack("!h", option))
            res = tcp.recv(2)
            if(not res):
                break
            else:
                status = struct.unpack("!h", res)[0]
                if(status == 1):
                    res = tcp.recv(8)
                    length = struct.unpack("!I", res)[0]
                    data = tcp.recv(4096)
                    if(not data):
                        break
                    else:
                        while(len(data) < length):
                            r = tcp.recv(4096)
                            if(not r):
                                break
                            else:
                                data+=r
                        data_json = json.loads(data.decode("utf-8"))
                        print(f"\t\tARQUIVO\t\t|\t\tTAMANHO(KB)\t\t")
                        print("-=-"*100)
                        for js in data_json.keys():
                            print(f"\t\t{js}\t\t|\t\t %.2f\t\t" %(data_json[js]/1024))
        elif(option == 2):
            tcp.send(struct.pack("!I", 2))
            res = tcp.recv(2)
            if(not res):
                break
            else:
                data = struct.unpack("!h", res)
                if(data == 1):
                    arq = input("Nome do arquivo: ").encode()
                    tcp.send("!I", len(arq))
                    tcp.send(arq)
            
            
            
                                
                    

if(__name__ == "__main__"):
    main()
