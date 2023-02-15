import os 
from socket import *
import threading
import colorama 
from colorama import Fore, Style

colorama.init()

serverName = "localhost"
serverPort = 8000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = "CONNECT"
clientSocket.send(message.encode())

username = ""
password = ""

def printCommands():
    print("---------------- SERVIDOR BATE-PAPO ----------------")
    print(f'| \033[93m{"LOGIN #username":20}\033[00m -> {"user login in server.":25} |')
    print(f'| \033[93m{"PASSWORD #password":20}\033[00m -> {"password login in server.":25} |')
    print(f'| \033[93m{"LIST":20}\033[00m -> {"list online rooms.":25} |')
    print(f'| \033[93m{"JOIN #room":20}\033[00m -> {"join in room.":25} |')
    print(f'| \033[93m{"EXIT":20}\033[00m -> {"leave the server.":25} |')
    print("----------------------------------------------------")

while True:
    response = clientSocket.recv(1024).decode()
    split_response = response.split()

    os.system("cls||clear")

    if split_response and split_response[0] == "CONNECTED":
        printCommands()
        while True:
            print("Command :", end = ' ')
            username = str(input()) # LOGIN username
            if username.split()[0] != "LOGIN":
                print(Fore.RED + 'Command Invalid.') 
                print(Style.RESET_ALL)
            else:
                break
        clientSocket.send(username.encode())

    elif split_response and split_response[0] == "USER_PASS":
        print("Welcome {}.".format(username.split()[1]))
        print("Server: user {}".format(split_response[1]))
        while True:
            print("Command :", end = ' ')
            password = str(input()) # PASSWORD password
            if password.split()[0] != "PASSWORD":
                print(Fore.RED + 'Command Invalid.') 
                print(Style.RESET_ALL)
            else:
                break
        message = password + ";" + username.split()[1]
        clientSocket.send(message.encode())

    elif split_response and split_response[0] == "LOGGED":
        print("User logged successful!")
        print("Server: password {}".format(split_response[1]))
        while True:
            print("Command :", end = ' ')
            message = str(input()) # LIST
            if message.split()[0] != "LIST":
                print(Fore.RED + 'Command Invalid.') 
                print(Style.RESET_ALL)
            else:
                break
        clientSocket.send(message.encode())

    elif split_response and split_response[0] == "ROOMS":
        print("ROOMS:\n")
        aRooms = split_response[1].split(";")
        for i in range(len(aRooms)):
            aRoomsFormatted = aRooms[i].split(".")
            print(f'{aRoomsFormatted[0]:10} {aRoomsFormatted[1]}', end=' ')
            print(Fore.GREEN + '(Online)')
            print(Style.RESET_ALL)

        while True:
            print("Command :", end = ' ')
            message = str(input()) # JOIN name_room
            if (message.split()[0] != "JOIN") or (message.split()[1] != "ROOM_1" and message.split()[1] != "ROOM_2" and message.split()[1] != "ROOM_3"):
                print(Fore.RED + 'Command Invalid.') 
                print(Style.RESET_ALL)
            else:
                break
        clientSocket.send(message.encode())
        break

os.system("cls||clear")

def receiveMessage():
    while True:
        message = clientSocket.recv(1024).decode()
        print(message)
    
def sendMessage():
    while True:
        clientSocket.send(input().encode())

threadReceive = threading.Thread(target=receiveMessage,args=()) 
threadSend = threading.Thread(target=sendMessage,args=())

threadReceive.start()
threadSend.start()
    