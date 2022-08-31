# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:19:49 2022

@author: heitor
"""

import socket
from threading import Thread
import os.path
import mimetypes

HOST, PORT = "localhost", 8004
CLRF = '/r/n'

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
        #headers = []
    
        if command == 'GET':
         #   for j, k in [i.split(':', 1) for i in temp [1:-1]]:
          #      headers[j.strip()] = k.strip()
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
                with open(file, "rb") as f:
                    file_bytes = f.read(1024)
                    
                    while(file_bytes):
                        self.connSocket.send(file_bytes)
                        file_bytes = f.read(1024)
                
        else:
            raise BadRequest('Not a GET request')
    
        self.connSocket.close()
    
                
    
def main():
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.bind((HOST, PORT))
    sSocket.listen(10)
    print("Server" +  HOST  + " is up and ready to receive")


    while(True):
        connSocket, addr = sSocket.accept()
        
        #print(connSocket.recv(1024).decode())
        
        request = HttpRequest(connSocket)
        
        request.start()
        
        request.join()
        
    sSocket.close()
      
                
    

if __name__ == "__main__":        
    main()