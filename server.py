import socket 
import threading

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
HELP_COMMAND = "/help"

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
    return "This is the list of commands: /join, /leave, /register /all and /msg"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
 
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            #COMMANDS
            to_client = ""
            if msg.startswith(LEAVE_COMMAND):
                connected = False
            elif msg.startswith(JOIN_COMMAND): 
                pass
            elif msg.startswith(REGISTER_COMMAND):
                pass
            elif msg.startswith(ALL_COMMAND):
                msg_to_client = msg.split(" ", 1)
                to_client = all(addr, msg_to_client[1])
            else:
                to_client = help()

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