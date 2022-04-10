import socket, threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    username = None #will be given a value when user logs in 
    #the variable will allow us to record when the user logs in and out of the server

    def send_messages(MSG: str):
        reply = MSG.encode(FORMAT)
        reply_length = len(reply)
        send_length = str(reply_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)#sends the length of the message so the program knows the size it is trying to receive
        conn.send(reply)

        
    def receive_messages():
        message_len = conn.recv(HEADER).decode(FORMAT)
        message_len = int(message_len)
        message = conn.recv(message_len).decode(FORMAT)

        return message
    try:
        while True:
            msg = receive_messages()
            print(f"NEW message from client {addr}")
            print(msg)
            if "Sign_up" in msg:
                pass
            elif "Login" in msg:

                while True:
                    msg = receive_messages()
                    #After user logs in the following are the commands they will have access to
                    
                    if "Send_Message" in msg:
                        pass
                    elif "Get_settings" in msg:
                        pass
                    elif "Edit_settings" in msg:
                        pass
                    elif "Review_profile" in msg:
                        pass
                    elif "Delete_message" in msg:
                        pass
                    elif " Logout" in msg:
                        pass
                    else:
                        send_messages("Not a vaild command")
            else:
                send_messages("Not a vaild command")
    except ConnectionResetError:
        print(f"Client {addr} has disconnected")

print("Server starting...")
server.listen()
print(f'Server is listening on {SERVER}')

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=client, args=(conn, addr))
    thread.start()
