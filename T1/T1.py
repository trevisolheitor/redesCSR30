# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:19:49 2022

@author: heitor
"""

import socket
from threading import Thread
import os.path
import mimetypes

PORT = 8004
CLRF = '\r\n'

class BadRequest(Exception):
    pass

class HttpRequest(Thread):
    def __init__(self, connSocket):
        Thread.__init__(self)
        self.connSocket = connSocket   
    
    def run(self):
       try:
           self.processRequest(self.connSocket)
       except Exception as e:    
           print(e)
                   
    def processRequest(self, connSocket):       
        data = self.connSocket.recv(1024).decode()   
        
        temp = [i.strip() for i in data.splitlines()]
        
        if -1 == temp[0].find("HTTP"):
            raise BadRequest    ('Incorrect Protocol')
            
        command, path, version = [i.strip() for i in temp[0].split()]
        if path == '/':
            path = '/index.html'
    
        if command == 'GET':
                file = path[1:]
                if (os.path.exists(file)):
                    contentType = mimetypes.guess_type(file)[0]
                    statusLine = "HTTP/1.0 200 OK" + CLRF                    
                    contentLine = "Content type: " +  contentType + CLRF                    

                else:
                    contentType = mimetypes.guess_type(file)[0]
                    statusLine = "HTTP/1.0 404 Not Found" + CLRF
                    contentLine = "Content type: " +  contentType + CLRF
                    file = "404.html"

                self.connSocket.send(statusLine.encode())
                self.connSocket.send(contentLine.encode())
		self.connSocket.send(CLRF)
                with open(file, "rb") as f:
                    self.connSocket.send(f.read())
                
        else:
            raise BadRequest('Not a GET request')
    
        self.connSocket.close()
    
#Função que retorna o IP da máquina, utilizado para criação do WebServer
#Código feito baseado no artigo sobre retorno de endereço IP com python do site DelftStack, disponível em: https://www.delftstack.com/howto/python/get-ip-address-python/
	
def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		s.connect(('8.8.8.8', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP
    
def main():
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #For Linux usage run the line below
    sSocket.bind((get_ip(), PORT))
    
    #For Windows usage run this other line below
    #sSocket.bind((socket.gethostbyname(socket.gethostname()), PORT))
    serveraddr = sSocket.getsockname()
    sSocket.listen(10)
    print("Server ", serveraddr[0], " on port ", serveraddr[1], " is up and ready to receive")

    try:
        while(True):
            connSocket, addr = sSocket.accept()
               
            request = HttpRequest(connSocket)
        
            request.start()
        
            request.join()
    except (KeyboardInterrupt):
        sSocket.close()
		
    sSocket.close()
      
                
    

if __name__ == "__main__":        
    main()
