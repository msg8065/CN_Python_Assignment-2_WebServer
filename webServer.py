# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(local_host="127.0.0.1", port=13331):
  # Create socket
  server_socket = socket(AF_INET, SOCK_STREAM)
  # Prepare server socket
  server_socket.bind((local_host, port))
  print(f"Using port: {port}")
  # Accept connections; 10 connection in backlog
  server_socket.listen(10)
  # Server run
  while True:
    print('Ready to serve...')
    # Accept an incoming connection request
    connection_socket, addr = server_socket.accept()
    try:
      # Receive the request message
      message = connection_socket.recv(1024).decode('utf-8')
      # Get the filename from the received message
      filename = message.split()[1]
      f = open(filename[1:], 'rb')
      file_data = f.read()
      # Prepare the HTTP 200 OK response header and add the file contents
      output_data = (
        "HTTP/1.1 200 OK\r\n"
        "Server: Computer Networks: Programming\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        "Connection: close\r\n\r\n"
      ).encode('utf-8') + file_data
      # Send HTTP header and file content in one send
      connection_socket.send(output_data)
      connection_socket.close()
    except Exception as e:
      # Send response message for invalid request due to the file not being found (404)
      error_message = b"<html><body><h1>404 Not Found</h1></body></html>"
      output_data = (
        "HTTP/1.1 404 Not Found\r\n"
        "Server: Computer Networks: Programming\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        "Connection: close\r\n\r\n"
      ).encode('utf-8') + error_message
      connection_socket.send(output_data)
      connection_socket.close()

if __name__ == "__main__":
  webServer()
