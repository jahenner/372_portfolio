from socket import *
serverName = "127.0.0.1"
serverPort = 982
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(f"Connected to: localhost on port: {serverPort}\nType /q to quit\nEnter message to send...")
client_message = input(">")
clientSocket.send(client_message.encode())
while client_message != "/q":
    if client_message == "/t":
            print("Select a square you are o")
            while client_message != "/q":
                pass  
    server_message = clientSocket.recv(1024).decode()
    print(server_message)
    client_message = input(">")
    clientSocket.send(client_message.encode())

clientSocket.close()