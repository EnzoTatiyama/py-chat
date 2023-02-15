import os 
from socket import *
import threading

os.system("cls||clear")

serverPort = 8000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen()
print("SERVER BATE-PAPO RUNNING...")

fileCreate = open("users.txt", "a")
fileCreate.close()

clientsLogged = []
clientsRoom_1 = []
clientsRoom_2 = []
clientsRoom_3 = []

def loginUser(aMsg):
    fileRead = open("users.txt", "r")
    lines = fileRead.readlines()
    fileRead.close()
    userExist = False
    response = ""

    for line in lines:
        if line.split(";")[0] == aMsg[1]:
            response = "USER_PASS ENTROU"
            userExist = True
            break

    if userExist != True:
        file = open("users.txt", "a")
        file.write(str(aMsg[1]) + ";")
        file.close()
        response = "USER_PASS CADASTRADO"
    return response

def loginPassword(aMsg, addr):
    fileRead = open("users.txt", "r")
    lines = fileRead.readlines()
    fileRead.close()
    passwordExist = False
    response = ""

    usernameClient = aMsg[1].split(";")[1]
    passwordClient = aMsg[1].split(";")[0]

    for line in lines:
        if line.split(";")[0] == usernameClient:
            if line.split(";")[1].strip() == passwordClient:
                response = "LOGGED ENTROU"
                passwordExist = True

    if passwordExist != True:
        fileWrite = open("users.txt", "a")
        fileWrite.write("{}\n".format(passwordClient))
        fileWrite.close()
        response = "LOGGED CADASTRADO"
    
    clientsLogged.append(str(addr[1]) + ";" + str(usernameClient))
    return response
        
def sendForAll(message, clients):
    for client in clients:
        client.send(message.encode())

def chatMessages(user, clients, username):
    while True:
        try: 
            receiveMessage = user.recv(1024).decode()
            messsage = f'{username} : {receiveMessage}'
            sendForAll(messsage, clients)
        except:
            user.close()

def room1(connectionSocket, addr):
    clientsRoom_1.append(connectionSocket)
    username = ""
    for idx in range(len(clientsLogged)):
        if str(clientsLogged[idx].split(";")[0]).strip() == str(addr[1]).strip():
            username = clientsLogged[idx].split(";")[1]
            break
    initialMessage = f'{username} joined the chat!'
    print(f'{addr} joined in Room 1.')
    sendForAll(initialMessage, clientsRoom_1)
    user_thread = threading.Thread(target=chatMessages, args=(connectionSocket,clientsRoom_1,username,))
    user_thread.start()

def room2(connectionSocket, addr):
    clientsRoom_2.append(connectionSocket)
    username = ""
    for idx in range(len(clientsLogged)):
        if str(clientsLogged[idx].split(";")[0]).strip() == str(addr[1]).strip():
            username = clientsLogged[idx].split(";")[1]
            break
    initialMessage = f'{username} joined the chat!'
    print(f'{addr} joined in Room 2.')
    sendForAll(initialMessage, clientsRoom_2)
    user_thread = threading.Thread(target=chatMessages, args=(connectionSocket,clientsRoom_2,username,))
    user_thread.start()

def room3(connectionSocket, addr):
    clientsRoom_3.append(connectionSocket)
    username = ""
    for idx in range(len(clientsLogged)):
        if str(clientsLogged[idx].split(";")[0]).strip() == str(addr[1]).strip():
            username = clientsLogged[idx].split(";")[1]
            break
    initialMessage = f'{username} joined the chat!'
    print(f'{addr} joined in Room 3.')
    sendForAll(initialMessage, clientsRoom_3)
    user_thread = threading.Thread(target=chatMessages, args=(connectionSocket,clientsRoom_3,username,))
    user_thread.start()

def multi_thread_client(connectionSocket, addr):
    while True:
        try:
            message = connectionSocket.recv(1024).decode()
            split_msg = message.split()

            if split_msg[0] == "CONNECT":
                print("Receive CONNECT")
                response = "CONNECTED"
                connectionSocket.send(response.encode())

            elif split_msg[0] == "LOGIN" or split_msg[0] == "login":
                connectionSocket.send(loginUser(split_msg).encode())

            elif split_msg[0] == "PASSWORD" or split_msg[0] == "password":
                connectionSocket.send(loginPassword(split_msg, addr).encode())

            elif split_msg[0] == "LIST" or split_msg[0] == "list":
                response = "ROOMS ROOM_1.[{}/10];ROOM_2.[{}/10];ROOM_3.[{}/10]".format(len(clientsRoom_1), len(clientsRoom_2), len(clientsRoom_3))
                connectionSocket.send(response.encode()) 

            elif split_msg[0] == "JOIN" or split_msg[0] == "join":
                if split_msg[1] == "ROOM_1":
                    room1(connectionSocket, addr)
                elif split_msg[1] == "ROOM_2":
                    room2(connectionSocket, addr)
                elif split_msg[1] == "ROOM_3":
                    room3(connectionSocket, addr)

            elif split_msg[0] == "EXIT":
                connectionSocket.close()
        except:
            pass

while 1:
    connectionSocket, addr = serverSocket.accept()
    print(f'Client {addr} connected.')
    threading.Thread(target=multi_thread_client, args=(connectionSocket,addr,)).start()
