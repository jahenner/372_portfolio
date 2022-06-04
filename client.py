# Alex Henner
# CS372
# Portfolio Project
# 6/4/22
# Sources: Computer Networking a Top Down Approach 7th edition Kurose, Ross

from socket import *
from server import print_board, STARTER, check_input, update_board

# Server info
serverName = "127.0.0.1"
serverPort = 982

# Client TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print(f"Connected to: localhost on port: {serverPort}\nType /q to quit or /t to play tic-tac-toe\nEnter message to send...")
client_message = input(">")
clientSocket.send(client_message.encode())
while client_message != "/q":
    # client wants to play a game :)
    if client_message == "/t":
        # print locations and receive blank board from server.
        print_board(STARTER)
        board = clientSocket.recv(1024).decode()
        client_message = input("Select a square you are o or type /q to quit back to chat\n>")
        
        while client_message != "/q":
            # Check to make sure selection is valid
            while not check_input(client_message, board):
                client_message = input("Please select a valid input\n>")
            clientSocket.send(client_message.encode())
            print_board(update_board(board, "o", int(client_message)))
            
            board = clientSocket.recv(1024).decode()
            if board == "/q":
                print("Server ended game")
                client_message = input("Enter message to send...\n>")
                break
            # After a win server sends back a message that starts with /end followed by winner X or O followed by board that won
            elif board[:4] == "/end":
                winner = board[4]
                print_board(board[5:])
                if winner == "X":
                    print("You lost")
                else:
                    print("You win!")
                print("\n\nWaiting on message from server...")
                server_message = clientSocket.recv(1024).decode()
                print(server_message)
                client_message = input(">")
                break
                
            print_board(board)
            
            client_message = input("Select a square you are o or type /q to quit back to chat\n>")
        
        # clean up to be able to go back to chat smoothly    
        clientSocket.send(client_message.encode())
        
    server_message = clientSocket.recv(1024).decode()
    print(server_message)
    client_message = input(">")
    clientSocket.send(client_message.encode())

# Close connection
clientSocket.close()