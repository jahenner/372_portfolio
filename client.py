from socket import *
from server import print_board, STARTER, check_input, update_board
serverName = "127.0.0.1"
serverPort = 982
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(f"Connected to: localhost on port: {serverPort}\nType /q to quit or /t to play tic-tac-toe\nEnter message to send...")
client_message = input(">")
clientSocket.send(client_message.encode())
while client_message != "/q":
    if client_message == "/t":
        print_board(STARTER)
        board = clientSocket.recv(1024).decode()
        client_message = input("Select a square you are o or type /q to quit back to chat\n>")
        
        while client_message != "/q":
            while not check_input(client_message, board):
                client_message = input("Please select a valid input\n>")
            clientSocket.send(client_message.encode())
            print_board(update_board(board, "o", int(client_message)))
            
            board = clientSocket.recv(1024).decode()
            if board == "/q":
                print("Server ended game")
                client_message = input("Enter message to send...\n>")
                break
            print_board(board)
            
            client_message = input("Select a square you are o or type /q to quit back to chat\n>")
            
        clientSocket.send(client_message.encode())
        
    server_message = clientSocket.recv(1024).decode()
    print(server_message)
    client_message = input(">")
    clientSocket.send(client_message.encode())

clientSocket.close()