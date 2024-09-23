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
            message = connectionSocket.recv(13331).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            # Send HTTP headers (corrected encoding)
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            # Send response message for file not found (404)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/plain\r\n\r\n".encode())
            connectionSocket.send("File not found.".encode())
            connectionSocket.close()
        except (ConnectionResetError, BrokenPipeError):
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
