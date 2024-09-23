GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
# Import necessary modules
from socket import *
import sys

def webServer(port=13331):
    # Create a TCP/IP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("localhost", port))
    serverSocket.listen(5)
    print(f"Server is running on port {port}...")

    while True:
        # Accept a new connection
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()  # Receive the request
            print(f"Received message: {message}")  # Debugging line
            filename = message.split()[1]  # Extract the filename from the request
            
            # Open the requested file
            with open(filename[1:], 'r') as f:  
                outputdata = f.read()

            # Send HTTP response headers
            connectionSocket.sendall("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.sendall("Content-Type: text/html\r\n".encode())
            connectionSocket.sendall("\r\n".encode())  # End of headers

            # Send the content of the requested file
            connectionSocket.sendall(outputdata.encode())

        except IOError:
            # Handle file not found error
            connectionSocket.sendall("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.sendall("Content-Type: text/plain\r\n".encode())
            connectionSocket.sendall("\r\n".encode())  # End of headers
            connectionSocket.sendall("File not found.".encode())
        except (ConnectionResetError, BrokenPipeError):
            print("Connection was reset or broken.")
        finally:
            connectionSocket.close()  # Close the connection

    serverSocket.close()
    sys.exit()  # Terminate the program

if __name__ == "__main__":
    webServer(13331)
