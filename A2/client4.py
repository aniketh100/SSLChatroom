import tkinter as tk
import socket
from googletrans import Translator, LANGUAGES


PORT = 4455
SIZE = 1024
FORMAT = "utf-8"

root = tk.Tk()
root.title("Translate from any language to English")

label_input = tk.Label(root, text="Enter text to translate:")
label_input.pack()

input_field = tk.Entry(root, width=50)
input_field.pack()

label_output = tk.Label(root, text="Translation:")
label_output.pack()

output_field = tk.Text(root, height=5, width=50)
output_field.pack()

label_language = tk.Label(root, text="Select input language:")
label_language.pack()

languages = list(LANGUAGES.values())

selected_language = tk.StringVar()
selected_language.set("English")

dropdown_language = tk.OptionMenu(root, selected_language, *languages)
dropdown_language.pack()

label_server_ip = tk.Label(root, text="Enter server IP address:")
label_server_ip.pack()

server_ip_field = tk.Entry(root, width=50)
server_ip_field.pack()

def translate(ip_address):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (ip_address, PORT)
    client.connect(ADDR)
    
    input_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(selected_language.get())]
    input_text = input_field.get()
    
    client.send(input_lang.encode(FORMAT))
    
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]:{msg}")


    client.send(input_text.encode(FORMAT))
    translated_text = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: Text to be translated recieved")
    

    output_field.delete(1.0, tk.END)
    output_field.insert(tk.END, translated_text)


    client.close()


button_translate = tk.Button(root, text="Translate", command=lambda: translate(server_ip_field.get()))
button_translate.pack()

root.mainloop()
