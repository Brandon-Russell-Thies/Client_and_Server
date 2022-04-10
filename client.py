from tkinter import *
import socket


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def main():
    def log():
        print("WORKS")
    def sign():
        send_messages("Testing")
        print(receive_messages())

    
    def send_messages(MSG: str):
        reply = MSG.encode(FORMAT)
        reply_length = len(reply)
        send_length = str(reply_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)#sends the length of the message so the program knows the size it is trying to receive
        client.send(reply)

        
    def receive_messages():
        message_len = client.recv(HEADER).decode(FORMAT)
        message_len = int(message_len)
        message = client.recv(message_len).decode(FORMAT)

        return message

    root = Tk()
    root.title("Login")
    sign_up = Button(root, text="Sign Up", command=sign)
    space = Label(root, text="                                                                      ")
    user = Label(root, text="Username")
    username = Entry(root)
    pas = Label(root, text="Password")
    password = Entry(root)
    login = Button(root, text="Login", command=log)
    error = Label(root, text="")
    sign_up.pack()
    space.pack()
    user.pack()
    username.pack()
    pas.pack()
    password.pack()
    login.pack()
    error.pack()

    root.mainloop()
main()
exit()