from tkinter import *
import socket


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
try:
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except:
    e = Tk()
    error_message = Label(e, text="Cannot connect to server")
    error_message.pack()
    e.mainloop()
    exit()



def main():
    
    
    def log():
        print("WORKS")
    
    
    def sign():
        send_messages("Testing")
        print(receive_messages())

    
    def send_messages(MSG: str):
        try:
            reply = MSG.encode(FORMAT)
            reply_length = len(reply)
            send_length = str(reply_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)#sends the length of the message so the program knows the size it is trying to receive
            client.send(reply)
        except ConnectionResetError:
            root.destroy()
            e = Tk()
            error_message = Label(e, text="Cannot connect to server")
            error_message.pack()
            e.mainloop()
            exit()#closes the program to keep more errors from happening

        
    def receive_messages():
        try:
            message_len = client.recv(HEADER).decode(FORMAT)
            message_len = int(message_len)
            message = client.recv(message_len).decode(FORMAT)

            return message
        except ConnectionResetError:
            root.destroy()
            e = Tk()
            error_message = Label(e, text="Cannot connect to server")
            error_message.pack()
            e.mainloop()
            exit()

    root = Tk()
    root.title("Login")
    sign_up = Button(root, text="Sign Up", command=sign)
    space = Label(root, text="                                                                      ")
    user = Label(root, text="Username")
    username = Entry(root)
    pas = Label(root, text="Password")
    password = Entry(root)
    login = Button(root, text="Login", command=log)
    error = Label(root, text="")#Allows for there to be deplayed an error to the user if something goes wrong
    
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
exit()#if we do not exit the code, the client will contiue to be connected to the server even after the GUI has been closed