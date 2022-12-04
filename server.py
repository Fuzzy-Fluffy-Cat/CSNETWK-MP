import socket 
import threading
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#COMMAND LIST
JOIN_COMMAND = "/join"
LEAVE_COMMAND = "/leave"
REGISTER_COMMAND = "/register"
ALL_COMMAND = "/all"
MSG_COMMAND = "/msg"
HELP_COMMAND = "/?"

#COMMAND FUNCTIONS
def join():
    pass

def leave():
    pass

def register():
    pass

def all(addr, msg):
    return f"[{addr}] {msg}"

def msg():
    pass

def help():
    return "\nThis is a list of commands\n/join - Join the chatroom\n/leave - Leave from the chatroom\n/register [alias] - Register to the chatroom\n/all [message] - Message all users\n/msg [alias] [message] - Message user with certain alias\n/? - Shows list of commands"

def no_user_input():
    return "Type /? for a list of commands..."

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def json_translator(message):
    data = json.loads(message)
    return data

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
 
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            print("msg from client: ")
            print(msg)
            print(json_translator(msg))
            
            #COMMANDS
            to_client = ""
            if msg.startswith(LEAVE_COMMAND):
                connected = False
            elif msg.startswith(JOIN_COMMAND): 
                pass
            elif msg.startswith(REGISTER_COMMAND):
                pass
            elif msg.startswith(ALL_COMMAND):
                msg_to_client = msg.split(" ", 1) #This splits /all and the encode
                to_client = all(addr, msg_to_client[1])
            elif msg.startswith(HELP_COMMAND):
                to_client = help()
            else:
                to_client = no_user_input()

            conn.send(to_client.encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()