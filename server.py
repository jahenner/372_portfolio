# Alex Henner
# CS372
# Portfolio Project
# 6/4/22
# Sources: Computer Networking a Top Down Approach 7th edition Kurose, Ross

from socket import *

STARTER = "123456789"
    
def print_board(board):
    result = "-------\n"
    for i in range(len(board)):
        if i % 3 == 0:
            result += "|"
        result += f"{board[i]}|" if board[i] != "_" else " |"
        if i % 3 == 2:
            result += "\n-------\n"
    print(result)
    
def update_board(board, player, location):
    board = board[:(location-1)] + player + board[location:]
    return board
    
def check_input(selection, board) -> bool:
    try:
        selection = int(selection)
        if 0 < selection <= 9 and board[selection-1] == "_":
            return True
        else:
            return False
    except TypeError:
        return False
    
def check_win(board):
    # horizontal
    for i in range(3):
        if "x" == board[3*i] == board[3*i+1] == board[3*i+2]:
            return "X"
        elif "o" == board[3*i] == board[3*i+1] == board[3*i+2]:
            return "O"
    
    # vertical
    for i in range(3):
        if "x" == board[i] == board[3+i] == board[6+i]:
            return "X"
        elif "o" == board[i] == board[3+i] == board[6+i]:
            return "O"
        
    # diagonals
        if "x" == board[0] == board[4] == board[8] or "x" == board[2] == board[4] == board[6]:
            return "X"
        elif "o" == board[0] == board[4] == board[8] or "o" == board[2] == board[4] == board[6]:
            return "O"
    
    return None

def main():
    # create server environment
    serverName = '127.0.0.1'
    serverPort = 982
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # bind the socket to the server environment
    serverSocket.bind((serverName, serverPort))

    # listen set to only allow 1 connection at a time
    serverSocket.listen(1)
    print(f'Server listening on: localhost port: {serverPort}')

    # make the process always on
    while True:
        # allow clients to connect and create new socket to send data
        connectionSocket, addr = serverSocket.accept()
        print(f"Connected by: {addr}\nWaiting on a message...")
        client_message = connectionSocket.recv(1024).decode()
        print("Type /q to quit or /t for tic-tac-toe\nEnter message to send...")
        while client_message != "/q":
            
            if client_message == "/t":
                # Create a blank board and send it to client
                board = "_"*9
                connectionSocket.send(board.encode())
                print_board(STARTER)
                
                # Update clients pick and show to server
                client_play = connectionSocket.recv(1024).decode()
                board = update_board(board, "o", int(client_play))
                print_board(board)
                server_message = input("Select a square or type /q to go back to chat. You will play as x.\n>")
                
                while server_message != "/q":
                    # Check move for validity and update board for server
                    while not check_input(server_message, board):
                        server_message = input("Please select a valid input\n>")
                    board = update_board(board, "x", int(server_message))
                    print_board(board)
                    
                    # Check to see if someone has won
                    is_win = check_win(board)
                    if is_win is not None:
                        if is_win == "X":
                            print("You win!")
                        else:
                            print("You lost")
                        board = "/end" + board
                        connectionSocket.send(board.encode())
                        server_message = input("Enter message to send...\n>")
                        break
                    
                    connectionSocket.send(board.encode())
                    client_play = connectionSocket.recv(1024).decode()
                    
                    # client doesn't want to play anymore :(
                    if client_play == "/q":
                        print("Client ended game")
                        server_message = input("Enter message to send...\n>")
                        break
                    
                    board = update_board(board, "o", int(client_play))
                    print_board(board)
                    
                    # game was updated so check again for winner
                    is_win = check_win(board)
                    if is_win is not None:
                        if is_win == "X":
                            print("You win!")
                        else:
                            print("You lost")
                        board = "/end" + is_win + board
                        connectionSocket.send(board.encode())
                        server_message = input("Enter message to send...\n>")
                        break
                    
                    server_message = input("Select a square or type /q to go back to chat. You will play as x.\n>")
                
                # smooth transition back to chat
                connectionSocket.send(server_message.encode())
                client_message = connectionSocket.recv(1024).decode()
                # client quit chat as well 
                if client_message == "/q": break
                
            print(client_message)
            server_message = input(">")
            connectionSocket.send(server_message.encode())
            client_message = connectionSocket.recv(1024).decode()
        
        # client connection closed and waiting for next client
        print("Connection Closed")
        connectionSocket.close()
        
if __name__ == "__main__":
    main()