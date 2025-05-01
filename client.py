import addrChat
import socket, os, sqlite3

#server config
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((addrChat.IP, addrChat.PORT))

os.system("clear")

while True:    
    #envia mensagem pro server
    message = input("> ")

    if not message:
        continue

    client.send(message.encode())
        
    #recebe mensagem do server
    if message.startswith('/'):
        response = client.recv(1024).decode()

        if response:
            print(response)

        if message.strip().lower() == "/exit":
            break


    