# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  
  #Prepare a server socket
  serverSocket.bind(("", port))
  
  #Fill in start
  serverSocket.listen(1)
  #Fill in end

  while True:
    #Establish the connection
    
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept() #Fill in start -are you accepting connections?     #Fill in end
    
    try:
      message = connectionSocket.recv(1024).decode() #Fill in start -a client is sending you a message   #Fill in end 
      filename = message.split()[1]
      
      #opens the client requested file. 
      #Plenty of guidance online on how to open and read a file in python. How should you read it though if you plan on sending it through a socket?
      f = open(filename[1:], 'rb')#fill in start #fill in end)
      #fill in end
      
      outputdata = b"Content-Type: text/html; charset=UTF-8\r\n"\
      #Fill in start -This variable can store your headers you want to send for any valid or invalid request.
      http_response = b""
      #Content-Type above is an example on how to send a header as bytes
      #Fill in end

      #Send an HTTP header line into socket for a valid request. What header should be sent for a response that is ok? 
      #Fill in start
      http_response = b"HTTP/1.1 200 OK\r\n"
      connectionSocket.send(http_response)
      connectionSocket.send(outputdata)
      #Fill in end

      #Send the content of the requested file to the client
      for i in f: #for line in file
        connectionSocket.send(i)#Fill in start - send your html file contents #Fill in end 
      connectionSocket.close() #closing the connection socket
      
    except Exception as e:
      # Send response message for invalid request due to the file not being found (404)
      #Fill in start
      http_response = b"HTTP/1.1 404 Not Found\r\n\r\n"
      connectionSocket.send(http_response)
      connectionSocket.send(outputdata)
      #Fill in end


      #Close client socket
      #Fill in start
      connectionSocket.close()
      #Fill in end

  serverSocket.close()
  sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
