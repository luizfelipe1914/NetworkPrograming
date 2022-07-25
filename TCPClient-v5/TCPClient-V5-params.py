#!/usr/bin/env python3

from operator import length_hint
import socket
import sys
import ssl

def create_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def wrap_soquete(sock, server):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context.wrap_socket(sock, server_hostname=server)

def send_http_POST(sock, server, resource, data):
    HTTP_POST = f"POST {resource} HTTP/1.1\r\nHost: {server}\r\nContent-Length: {len(data)}\r\n\r\n{data}"
    sock.sendall(HTTP_POST.encode())
    
def send_http_GET(sock, server, resource):    
    HTTP_GET = f"GET {resource} HTTP/1.1\r\nHost: {server}\r\n\r\n"
    sock.sendall(HTTP_GET.encode())
    
def get_body_contentLength(body, sock, length_body):
    while(len(body) < length_body):
        body+=sock.recv(4096)
    return body

def get_body_chunked(response, sock):
    body = b""
    end_length = response.find(b"\r\n")
    length_chunked = int(response[:end_length], 16)
    while(length_chunked > 0):
        response = response[end_length+2:]
        while(len(response) < length_chunked):
            response += sock.recv(4096)
        body += response[:length_chunked]
        response = response[length_chunked+2:]
        end_length = response.find(b"\r\n")
        while(end_length == -1):
            response+=sock.recv(4096)
            end_length = response.find(b"\r\n")
        length_chunked = int(response[:end_length], 16)
    return body
  
def getResponse(sock):
    buffer = sock.recv(4096)
    end_headers = buffer.find(b"\r\n\r\n")
    headers = buffer[:end_headers]
    body = buffer[end_headers+4:]
    for header in headers.split(b"\r\n"):
        if(header.startswith(b"Content-Length:")):
            length_body = int(header.split(b":")[1])
            body = get_body_contentLength(body, sock, length_body)
            break
        elif(headers.startswith(b"Transfer-Encoding:")):
            body = get_body_chunked(body, sock)
            break
    return body

def read_parameters_from_file(file):
    try:
        with open(file) as f:
            data = f.read()
            f.close()
    except Exception as err:
        print(err)
    return data   

def read_parameters_from_cli():
    data = ""
    try:
        if(len(sys.argv) == 8):
            data = sys.argv[7]
    except Exception as err:
        print(err)
    return data

def write_data(file_name, data):
    try:
        with open(file_name, "wb") as file:
            file.write(data)
    except Exception as err:
        print(err)

def get_cli_parameters():
    parameters = {}
    if(len(sys.argv) >= 6 ):
        parameters["HOST"] = sys.argv[1]
        parameters["PORT"] = int(sys.argv[2])
        parameters["RESOURCE"] = sys.argv[3]
        parameters["-o"] = sys.argv[4]
        parameters["OUTPUT_FILE"] = sys.argv[5]
        if(len(sys.argv) == 8):
            parameters["flag"] = sys.argv[6]
            parameters["INPUT"] = sys.argv[7]
    return parameters
           

def main():
    param = get_cli_parameters()
    if(len(param) == 5 and param["-o"] == "-o"):
        
        if(param["PORT"] == 80):
            sock = create_socket(param["HOST"], param["PORT"])
            send_http_GET(sock, param["HOST"], param["RESOURCE"])
            body = getResponse(sock)
            write_data(param["OUTPUT_FILE"], body)
            
        elif(param["PORT"] == 443):
            sock = wrap_soquete(create_socket(param["HOST"], param["PORT"]), param["HOST"])
            send_http_GET(sock, param["HOST"], param["RESOURCE"])
            body = getResponse(sock)
            write_data(param["OUTPUT_FILE"], body)
            
    elif(len(param) == 7):
        if(param["flag"] == "-p"):
            data = read_parameters_from_cli()          
        elif(param["flag"] == "-f"):
            data = read_parameters_from_file(param["INPUT"])
        else:
            print(f"Sintaxe Incorreta!\n python TCPClient-V5-params.py <HOST> <PORT>  <RESOURCE> -o <OUTPUT FILE>  [ -p <DADOS> | -f <INPUT FILE> ]")        
        if(param["PORT"] == 80):
            sock = create_socket(param["HOST"], param["PORT"])
            send_http_POST(sock, param["HOST"], param["RESOURCE"], data)
            body = getResponse(sock)
            write_data(param["OUTPUT_FILE"], body)
        elif(param["PORT"] == 443):
            sock = wrap_soquete(create_socket(param["HOST"], param["PORT"]), param["HOST"])
            send_http_POST(sock, param["HOST"], param["RESOURCE"], data)
            body = getResponse(sock)
            write_data(param["OUTPUT_FILE"], body)
    else:
        print(f"Sintaxe Incorreta!\n python TCPClient-V5-params.py <HOST> <PORT>  <RESOURCE> -o <OUTPUT FILE>  [ -p <DADOS> | -f <INPUT FILE> ]")        
                    
    
if(__name__ == "__main__"):
    main()