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
            print(f"Received message: {message}")  # Debugging line to see the received message
            
            # Check if the message is empty or malformed
            if not message:
                raise ValueError("Empty message received")
            
            # Extract the filename from the request
            request_line = message.splitlines()[0]  # Get the first line of the request
            filename = request_line.split()[1]  # Extract the filename
            
            # Open file in read mode using context manager
            with open(filename[1:], 'r') as f:  
                outputdata = f.read()

            # Send HTTP headers
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n".encode())
            connectionSocket.send("\r\n".encode())  # Ensure headers are terminated

            # Send the content of the requested file to the client
            connectionSocket.send(outputdata.encode())  # Send entire content at once

        except IOError:
            # Send response message for file not found (404)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/plain\r\n".encode())
            connectionSocket.send("\r\n".encode())  # Ensure headers are terminated
            connectionSocket.send("File not found.".encode())
        except (ConnectionResetError, BrokenPipeError):
            pass
        except ValueError as ve:
            print(f"ValueError: {ve}")  # Log the error for debugging
        finally:
            connectionSocket.close()  # Ensure the connection is closed after each request

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
