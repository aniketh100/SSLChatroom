import socket, ssl
import threading

HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)
ssl_socket.connect((HOST, PORT))

def handle_messages():
    while True:
        data = ssl_socket.recv(BUFFER_SIZE)
        if not data:
            break
        message = data.decode('utf-8')
        print(message)

threading.Thread(target=handle_messages).start()

while True:
    message = input("> ")
    ssl_socket.send(message.encode('utf-8'))
