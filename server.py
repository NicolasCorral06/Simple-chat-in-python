import addrChat
import socket, sqlite3
#from threading import Thread

exit = 0;

#sql config
conn = sqlite3.connect(".chat.db")
cursor = conn.cursor()

#cursor.execute(<comando sql>)

#server config
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
#reutilza o socket caso esteja em aberto

server.bind((addrChat.IP, addrChat.PORT))
server.listen()

#functions
def list_commands():
    commands = """
/help - Lista todos os comandos
/login <nome_user> - Faz login na conta selecionada
    Caso não tenha conta, perguntara se quer criar
/join - Entra em um chat
/create - Cria um chat
/exit - Fecha o chat
    """
    return commands

def command_verify(message, client):
    if not message.startswith('/'):
        return message
    
    else:
        command, *args = message[1:].split()  # Remove '/' e divide
        args = ' '.join(args)  # Junta os argumentos
        
        match command:
            case "help": 
                help_text = list_commands()
                client.send(help_text.encode())
                return "help"
            
            case "exit":
                exit_text = "Desconectando...."
                client.send(exit_text.encode())
                return "exit"
            
            case _:
                client.send(f"SERVER - Comando desconhecido: {command}".encode())
                return None

#main code
while True:
    client, addr = server.accept()
    print(f"SERVER - Conexão criado por {addr} com sucesso") #Conexão do client com sucesso

    while True:
        message = client.recv(1024).decode() #Recebe mensagem e confirma ela

        #FIXME
        #Quando o client desconecta ele da automaticamente da essa mensagem
        if message == "": #falha no sistema
            print("SERVER - Overflow de mensagem")
            break

        print(f"CLIENT MESSAGE - {addr} enviou: {message}")
        result = command_verify(message, client)

        if result != None:

            match result: # Mensagens expecificas
                case "exit":
                    print(f"SERVER - {addr} Desconectou do server") #Conexão encerrada do client
        