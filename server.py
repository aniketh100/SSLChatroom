import threading
import socket, ssl

HOST = '192.168.181.44'
PORT = 8080
BUFFER_SIZE = 1024
MAX_CONNECTIONS = 4

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CONNECTIONS)
clients = []
def handle_client_connection(conn, addr):
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
        except:
            data = None
        if not data:
            break
        message = f"{addr}: {data.decode('utf-8').strip()}"
        print(message)
        for client in clients:
            client.send(message.encode('utf-8'))


    conn.close()
    clients.remove(conn)
    print(f"Client {addr} disconnected.")

print(f"Server is listening on {PORT}")
while True:
    conn, addr = server_socket.accept()


    conn = context.wrap_socket(conn, server_side=True)

    clients.append(conn)

    threading.Thread(target=handle_client_connection, args=(conn, addr)).start()
