import socket
import threading
import random

PORT = 55555
SERVER = '192.168.254.108'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((SERVER, random.randint(8000, 9000)))

#COMMAND LIST
JOIN_COMMAND = "/join"
LEAVE_COMMAND = "/leave"
REGISTER_COMMAND = "/register"
ALL_COMMAND = "/all"
MSG_COMMAND = "/msg"
HELP_COMMAND = "/?"

#Receives stuff from server
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

#Sends stuff to server. We code here.
def command_to_json(command, argument, name):
    if command.startswith(LEAVE_COMMAND):
        return b'{ "command": "/leave" }'
        
    elif command.startswith(JOIN_COMMAND): 
        str = '{ "command": "/join", "owner": "'+ name +'" }'
        return bytes(str, 'utf-8')

    elif command.startswith(REGISTER_COMMAND):
        alias = argument
        str = '{ "command": "/register", "alias": "'+ alias +'" }'
        return bytes(str, 'utf-8')

    elif command.startswith(ALL_COMMAND):
        msg_to_client = argument
        message = '{ "command": "/all", "owner": "'+ name +'", "message": "' + msg_to_client + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(MSG_COMMAND):
        argument = argument.split(" ", 1)
        message = '{ "command": "/msg", "owner": "'+ name +'", "message": "' + argument[1] + '", "client: "' +  argument[0] + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(HELP_COMMAND):
        return b'{ "command": "/?" }'
    
    else:
        return b'{ "command": "" }'

name = ""
print("Type /register [alias] to start")
while True:
    message = input("")

    input_tokens = message.split(" ", 1)
    command = input_tokens[0]

    argument = ""
    if len(input_tokens) > 1:
        argument = input_tokens[1]
    
    if message.startswith(LEAVE_COMMAND):
        exit()
    elif message.startswith(REGISTER_COMMAND) and argument != "":
        name = argument
        print("Welcome " + name) 
    elif message.startswith(HELP_COMMAND):
        print("\nThis is a list of commands\n/join - Join the chatroom\n/leave - Leave from the chatroom\n/register [alias] - Register to the chatroom\n/all [message] - Message all users\n/msg [alias] [message] - Message user with certain alias\n/? - Shows list of commands")
    elif not message.startswith(JOIN_COMMAND) and not message.startswith(ALL_COMMAND) and not message.startswith(MSG_COMMAND):
        print("Type /? for a list of commands...")
    elif not name == "":
        json_message = command_to_json(command, argument, name)
        client.sendto(json_message, ADDR)
    else:
        print("Type /register [alias] to start")

#test