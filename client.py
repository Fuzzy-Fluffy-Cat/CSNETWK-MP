import socket
import json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.254.108"
ADDR = (SERVER, PORT)

#COMMAND LIST
JOIN_COMMAND = "/join"
LEAVE_COMMAND = "/leave"
REGISTER_COMMAND = "/register"
ALL_COMMAND = "/all"
MSG_COMMAND = "/msg"
HELP_COMMAND = "/?"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def command_to_json(command, argument):
    if command.startswith(LEAVE_COMMAND):
        return b'{ "command" : "/leave" }'
        
    elif command.startswith(JOIN_COMMAND): 
        return b'{ "command" : "/join" }'

    elif command.startswith(REGISTER_COMMAND):
        alias = argument   #command.split(" ", 1)[1]
        str = '{ "command":"/register", "alias": "'+ alias +'"}'
        return bytes(str, 'utf-8')

    elif command.startswith(ALL_COMMAND):
        msg_to_client = argument   #command.split(" ", 1) #This splits /all and the message
        message = '{ "command": "/all", "message": "' + msg_to_client[1] + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(HELP_COMMAND):
        return b'{ "command" : "/?" }'

    else:
        return b'{ "command" : "" }'

def send(input):
    #message = msg.encode(FORMAT)
    #send_length += b' ' * (HEADER - len(send_length))
    
    print(input)
    input_tokens = input.split(" ", 1)
    command = input_tokens[0]
    argument = input_tokens[1]
  
    json_message = command_to_json(command, argument)

    msg_length = len(json_message)
    send_length = str(msg_length).encode(FORMAT)
    
    print(json_message)

    client.send(send_length)
    client.send(json_message)

    print(client.recv(2048).decode(FORMAT))

input = ""
while(input != LEAVE_COMMAND):
    input = input("$ ")
    send(input)
