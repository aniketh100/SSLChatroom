import socket
import threading
from googletrans import Translator, LANGUAGES


IP = socket.gethostbyname(socket.gethostname()) #not assigned by the user/dynamic
PORT = 4455
ADDR = (IP,PORT)
translator = Translator()
FORMAT = "utf-8" #ASCII type
SIZE = 1024

def handle_client(conn, addr):
    
    print(f"[NEW CONNECTION] {addr} connected.")

    input_lang= conn.recv(SIZE).decode(FORMAT)

    print(f"[RECV] {input_lang} received.")
    file = open("server_data/"+input_lang+".txt","a+")

    conn.send("Input Lang received.".encode(FORMAT))

    data = conn.recv(SIZE).decode(FORMAT)

    print(f"[RECV] Text to be translated received.")
    file.write("\n"+input_lang+";"+data)
    translated_text = translator.translate(data, src=input_lang)

    conn.send(translated_text.text.encode(FORMAT))
    conn.close()
    file.close()
    print(f"[DISCONNECTED] {addr} disconnected")


def main():
    print("[STARTING] Server is starting.")
    print(f"[STARTING] Server is starting on {IP}:{PORT}")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP CONNECTION
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
