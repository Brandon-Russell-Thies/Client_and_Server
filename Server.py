import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")


    def send_message(MSG: str):
        reply = MSG.encode(FORMAT)
        reply_length = len(reply)
        send_length = str(reply_length).encode[FORMAT]
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(reply)

    def receive_message():
        message_len = conn.recv(HEADER).decode(FORMAT)
        message_len = len(message_len)
        message = conn.recv(message_len.decode(FORMAT))

        return message
    msg = receive_message()
    while True:
        if "Sign_up" in msg:
            pass
        elif "Login" in msg:
            while True:
                msg = receive_message()

                
                if "Send_Message" in msg:
                    pass
                elif "Get_settings" in msg:
                    pass
                elif "Edit_settings" in msg:
                    pass
                elif "Review_profile":
                    pass
                elif "Delete_message":
                    pass
                else:
                    send_message("Not a vaild command")
        else:
            send_message("Not a vaild command")
    
print("Server starting...")
server.listen()
print(f'Server is listening on {SERVER}')

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=client, args=(conn, addr))
    thread.start()
