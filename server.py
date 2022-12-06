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
    #Address already exists in the server
    if addr in clients:
      msg_to_send = "[Error] You are already connected to the server!".encode()
      msg(msg_to_send, addr)
    #Alias already exists in the server
    elif message['owner'] in [*clients.values()]:
      msg_to_send = f"[Error] The alias \"{message['owner']}\" already exists. Register a new one".encode()
      msg(msg_to_send, addr)
    
    else: #Successfully Connected
      clients[addr] = message['owner']
      msg_to_send = f"---{message['owner']} has joined the server---".encode()
      all(message, msg_to_send)
    
def all(message, msg_to_send):
    global clients
  
    for client_addr, client_name in clients:
      if client_name != message['owner']: 
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
      msg_to_send = f"---\"{old_name}\" has renamed himself as \"{new_name}\"---".encode()
      all(message, msg_to_send)
    
    #Alias already exists
    else:
      msg_to_send = f"[Error] The alias \"{message['owner']}\" already exists. Register a new one".encode()
      msg(msg_to_send, addr)
      

def leave(addr, message):
    global clients
    
    #Not connected to the server
    if addr not in clients:
        msg_to_send = "[Error] You are not connected to a server".encode()
        msg(msg_to_send, addr)
    else:
        msg_to_all = f"---{message['owner']} has disconnected from the server---".encode()
        msg_to_self = "---You have disconnected from the server---".encode()
        all(message, msg_to_all)
        msg(msg_to_self, addr)


def broadcast():
    global clients
  
    msg_to_send = ""
    while True:
        while not messages.empty():
            message, addr = messages.get()

            print(message)
            print(addr)

            message = json.loads(message.decode())
            print(message)
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
                        receiver = [a for a, u in clients.items() if u == message['receiver']]  #Gets the address corresponding to the alias
                        
                        msg(msg_to_send, receiver)
                    else:
                        msg_to_send = f"[Error] The receiver \"{message['receiver']}\" does not exist.".encode()
                        msg(msg_to_send, addr)
                elif message['command'] == REGISTER_COMMAND:
                    register(addr, message)
                elif message['command'] == LEAVE_COMMAND:
                    leave(addr, message)
                else:
                    pass
            except:
                del clients[addr]

def start():
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")

    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=broadcast)

    t1.start()
    t2.start()

start()