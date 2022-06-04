from socket import *


def print_board(board):
    result = "-------\n"
    for row in board:
        result += "|"
        for col in row:
            result += f"{col}|"
        result += "\n-------\n"
    print(result)

# create server environment
serverName = '127.0.0.1'
serverPort = 982
serverSocket = socket(AF_INET, SOCK_STREAM)

# bind the socket to the server environment
serverSocket.bind((serverName, serverPort))

# listen set to only allow 1 connection at a time
serverSocket.listen(1)
print(f'Server listening on: localhost port: {serverPort}')
board = [[' ']*3]*3
starter = []

print_board(board)
# make the process always on
while True:
    # allow clients to connect and create new socket to send data
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected by: {addr}\nWaiting on a message...")
    client_message = connectionSocket.recv(1024).decode()
    print("Type /q to quit or /t for tic-tac-toe\nEnter message to send...")
    while client_message != "/q":
        if client_message == "/t":
            tic_tac_toe_message = "Select a square. You will play as x.\n\n"
            
            connectionSocket.send(tic_tac_toe_message.encode())
            while client_message != "/q":
                pass        
        print(client_message)
        server_message = input(">")
        connectionSocket.send(server_message.encode())
        client_message = connectionSocket.recv(1024).decode()
    
    print("Connection Closed")
    connectionSocket.close()