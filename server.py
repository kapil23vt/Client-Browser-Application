import sys
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

# Create socket at port 80 and keep on listening
serverPort = 80
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    print('Server is ready to accept the connections!')

    #Establish the connection
    connectionSocket, addr = serverSocket.accept() 

    try:
        message = connectionSocket.recv(1024)  
        # print(message)
        filename = message.split()[1]
        print(filename)
        
        # Add encoding specification
        f = open(filename[1:], encoding="utf8")
        outputdata = f.read() 
        print(outputdata)
        
        connectionSocket.send(b'\n')
        connectionSocket.send(b'HTTP/1.1 200 OK\n')
        connectionSocket.send(b'Connection: close\n')
        
        totalMessageLength = 'Content-Length: '+str(len(outputdata))+'\n'
        
        connectionSocket.send(bytes(totalMessageLength, encoding="utf8"))
        connectionSocket.send(b'Content-Type: text/html\n')
        connectionSocket.send(b'\n')
        connectionSocket.send(b'\n')

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:

        #Send response message for file not found
        connectionSocket.send(b'\n')
        connectionSocket.send(b'404 Error: Document not found')
        connectionSocket.close()


serverSocket.close()

#Terminate the program after sending the corresponding data
sys.exit()
