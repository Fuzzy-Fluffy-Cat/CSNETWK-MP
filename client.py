import socket
import threading
import random
from datetime import datetime
import pytz

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((SERVER, random.randint(8000, 9000)))

#Temporary username/alias


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

# #Checks if there are no error in num of args
# def no_args_amt_error(command, argument):
#     if command.startswith(MSG_COMMAND):
        
#         if len(argument):
#             return 0
      
#     if command.startswith(LEAVE_COMMAND):
#         if not len(argument):
#             return 0
        
#     if command.startswith(JOIN_COMMAND): 
#         return ""

#     if command.startswith(REGISTER_COMMAND):
        

#     if command.startswith(ALL_COMMAND):
        

    
        

#     if command.startswith(HELP_COMMAND):
        
    
#     return 1


#Sends stuff to server. We code here.
def command_to_json(command, argument):
    global name
    if command.startswith(LEAVE_COMMAND):
        str = '{ "command": "/leave" , "owner": "'+ name +'"}'
        return bytes(str, 'utf-8')
        
    elif command.startswith(JOIN_COMMAND): 
        str = '{ "command": "/join", "owner": "'+ name +'" }'
        return bytes(str, 'utf-8')

    elif command == REGISTER_COMMAND:
        alias = argument
        str = '{ "command": "/register", "owner": "'+ name +'", "alias": "'+ alias +'" }'
        name = alias
        return bytes(str, 'utf-8')

    elif command.startswith(ALL_COMMAND):
        msg_to_client = argument
        message = '{ "command": "/all", "owner": "'+ name +'", "message": "' + msg_to_client + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(MSG_COMMAND):
        argument = argument.split(" ", 1)
        message = '{ "command": "/msg", "owner": "'+ name +'", "message": "' + argument[1] + '", "receiver": "' +  argument[0] + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(HELP_COMMAND):
        return b'{ "command": "/?" }'
    
    else:
        return b'{ "command": "" }'


name = "user_" + datetime.now(pytz.timezone('Singapore')).strftime("%d%m%Y%H%M%S")
# print(f"\"{name}\" has been set as your temporary name. Use the /register command to register a new name.")
print("Use the /join command to connect to a server.")
print('server '+SERVER)

joined = False
while joined == False:
    i = input("")
    j = "/join " + SERVER + " " + str(PORT)
    joined = True if i == j else False
    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.") if joined == False else print(f"\"{name}\" has been set as your temporary name. Use the /register command to register a new name.")

while True:
    message = input(f"{name}: ")

    input_tokens = message.split(" ", 1)
    command = input_tokens[0]

    argument = ""
    if len(input_tokens) > 1:
        argument = input_tokens[1]
    
    if message.startswith(HELP_COMMAND):
        print("\nThis is a list of commands\n/join - Join the chatroom\n/leave - Leave from the chatroom\n/register [alias] - Register to the chatroom\n/all [message] - Message all users\n/msg [alias] [message] - Message user with certain alias\n/? - Shows list of commands")

    elif message.startswith(JOIN_COMMAND) or message.startswith(ALL_COMMAND) or message.startswith(MSG_COMMAND) or message.startswith(REGISTER_COMMAND) or message.startswith(LEAVE_COMMAND):
        json_message = command_to_json(command, argument) 
        print(json_message)
        client.sendto(json_message, ADDR)
    
    else:
        #Error message for unrecognized command
        print(f"{command} is not recognized as a command by the program.\nPlease type \"/?\" for a list of commands.")  