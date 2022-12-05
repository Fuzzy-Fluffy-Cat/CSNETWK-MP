import socket 
import threading
import queue
import json

PORT = 55555
SERVER = '192.168.254.108'
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
clients = []

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except: 
            pass

#COMMAND FUNCTIONS
def join(server, client, message):
    server.sendto(f"{message['owner']} joined!".encode(), client)
    
def all(server, client, message):
    server.sendto(f"{message['owner']}: {message['message']}".encode(), client)

def msg():
    pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            message = json.loads(message.decode())
            print(message)
            print("Command Used: " + message['command'])
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message['command'] == JOIN_COMMAND:
                        join(server, client, message)
                    elif message['command'] == ALL_COMMAND:
                        all(server, client, message)
                    elif message['command'] == MSG_COMMAND:
                        pass
                    else:
                        pass
                except:
                    clients.remove(client)

def start():
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")

    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=broadcast)

    t1.start()
    t2.start()

start()