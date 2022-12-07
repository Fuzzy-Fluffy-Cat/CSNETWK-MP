import socket 
import threading
import queue
import json

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

#COMMAND LIST
JOIN_COMMAND = "/join"
LEAVE_COMMAND = "/leave"
REGISTER_COMMAND = "/register"
ALL_COMMAND = "/all"
MSG_COMMAND = "/msg"
HELP_COMMAND = "/?"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

messages = queue.Queue()
clients = {}

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except: 
            pass

#COMMAND FUNCTIONS
def join(addr, message):
    global clients
    if addr in clients: #Address already exists in the server
        msg_to_send = "Error: You are already connected to the server!".encode()
        msg(msg_to_send, addr)
    
    elif message['owner'] in [*clients.values()]: #Alias already exists in the server
        msg_to_send = f"Error: The alias \"{message['owner']}\" already exists. Register a new one".encode()
        msg(msg_to_send, addr)
    
    elif message['server'] == SERVER and message['port'] == str(PORT): #Successfully Connected
        clients[addr] = message['owner']

        #Server Message to all; new client connected
        msg_to_send = f"--- {message['owner']} has joined the server ---".encode()
        all(message, msg_to_send)
        #Server message to the one who successfully joined
        msg_to_self = f"--- You have successfully joined the server (Server Add.: {SERVER})".encode()
        msg(msg_to_self, addr)
    
    else: # Catch Error
        print('Error: Use /join <server_ip_add> <port>')
    
def all(message, msg_to_send):
    global clients
  
    for client_addr, client_name in clients.items():
        if client_name != message['owner']: 
            msg(msg_to_send, client_addr)
        else: # To sender
            msg_to_send = f"[To everyone]: {message['message']}".encode()
            msg(msg_to_send, client_addr)

def msg(msg_to_send, receiver):
    global server
    server.sendto(msg_to_send, receiver)

def register(addr, message):
    global clients
    
    #Success Register
    if message['alias'] not in [*clients.values()]:
        old_name = message['owner']
        new_name = message['alias']
        clients[addr] = new_name
        msg_to_send = f"--- \"{old_name}\" has renamed themselves as \"{new_name}\" ---".encode()
        all(message, msg_to_send)
    
    #Alias already exists
    else:
        msg_to_send = f"Error: The alias \"{message['owner']}\" already exists. Register a new one.".encode()
        msg(msg_to_send, addr)

def leave(addr, message):
    global clients
    
    #Not connected to the server
    # if addr not in clients:
    #     msg_to_send = "Error: You are not connected to a server!".encode()
    #     msg(msg_to_send, addr)
    # else:
    msg_to_all = f"--- {message['owner']} has disconnected from the server--- ".encode()
    msg_to_self = "--- You have disconnected from the server--- ".encode()
    all(message, msg_to_all)
    msg(msg_to_self, addr)
    del clients[addr]

def broadcast():
    global clients
    msg_to_send = ""

    while True:
        while not messages.empty():
            print('clients', clients)
            message, addr = messages.get()

            # print('msg:',message)
            print('addr',addr)

            message = json.loads(message.decode())
            print('msg:',message)
            print("Command Used: " + message['command'])
            try:
                if message['command'] == JOIN_COMMAND:
                    join(addr, message)
                elif message['command'] == ALL_COMMAND:
                    msg_to_send = f"[To everyone] {message['owner']}: {message['message']}".encode()
                    all(message, msg_to_send)
                elif message['command'] == MSG_COMMAND:
                    if message['receiver'] in [*clients.values()]:
                        msg_to_send = f"[To You] {message['owner']}: {message['message']}".encode()
                        receiver = [a for a, u in clients.items() if u == message['receiver']][0]  #Gets the address corresponding to the alias
                        msg(msg_to_send, receiver)
                        msg_to_self = f"[To {message['receiver']}]: {message['message']}".encode()
                        msg(msg_to_self, addr)
                    elif message['receiver'] == "invalidreceivercode":
                        msg_to_send = f"Error: Use /msg <receiver> <msg> to send a message.".encode()
                        msg(msg_to_send, addr)
                    else:
                        msg_to_send = f"Error: The receiver \"{message['receiver']}\" does not exist.".encode()
                        msg(msg_to_send, addr)
                elif message['command'] == REGISTER_COMMAND:
                    register(addr, message)
                elif message['command'] == LEAVE_COMMAND:
                    leave(addr, message)
                else:
                    pass
            except:
                pass

def start():
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")

    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=broadcast)

    t1.start()
    t2.start()

start()