# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.bind(("localhost", port))
    serverSocket.listen(5)

    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()  # Adjusted buffer size
            filename = message.split()[1]
            f = open(filename[1:], 'r')  # Open file in read mode
            outputdata = f.read()

            # Send HTTP headers as a single string
            headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            connectionSocket.send(headers.encode())
            # Send the content of the requested file to the client
            connectionSocket.send(outputdata.encode())  # Send entire content at once

            connectionSocket.close()
        except IOError:
            # Send response message for file not found (404)
            headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n"
            connectionSocket.send(headers.encode())
            connectionSocket.send("File not found.".encode())
            connectionSocket.close()
        except (ConnectionResetError, BrokenPipeError):
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
