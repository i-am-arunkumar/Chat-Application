from socket import AF_INET, SOCK_STREAM, socket
from tkinter import *
import threading
from tkinter import messagebox
import datetime
import sys

FORMAT = 'utf8'

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)


class GUI:
    # constructor method

    def __init__(self):
        # chat window which is currently hidden

        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=350,
                             height=300)
        self.login.configure(bg="#551111")
        # create a Label
        self.pls = Label(self.login,
                         text="LET'S CHAT!\n Enter Name To Continue:",
                         justify=CENTER,
                         font="Helvetica 16 bold", bg="#551111",
                         fg="#EAECEE")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)

        self.labelName = Label(self.login,
                               text="NAME:",
                               font="Helvetica 14 bold", bg="#551111",
                               fg="#EAECEE")

        self.labelName.place(relheight=0.1,
                             relx=0.1,
                             rely=0.4)

        self.icon = PhotoImage(file=r"chat.png")
        self.iconLabel = Label(self.login, image=self.icon, bg="#551111")
        self.iconLabel.place(relx=0.10,
                             rely=0.65)
        """self.labelPass = Label(self.login,
                               text="PASSWORD:",
                               font="Times 14 bold", bg="#ffcc99")
        self.labelPass.place(relheight=0.1,
                             relx=0.1,
                             rely=0.40)"""
        self.entryName = Entry(self.login)

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.45,
                             rely=0.4)

        self.entryName.focus()

        # create a Continue Button
        # along with action

        self.go = Button(self.login,
                         text="LOGIN",
                         font="Helvetica 14 bold", bg="#113311", fg="#EAECEE",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.flash()

        self.go.place(relx=0.4,
                      rely=0.60)
        
        self.Window.protocol("WM_DELETE_WINDOW", self.EXIT)

        self.login.bind(
            '<Return>', lambda e: self.goAhead(self.entryName.get()))
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        self.client = socket(AF_INET, SOCK_STREAM)
        print(ADDR)
        self.client.connect(ADDR)
        self.stop = False
        self.rcv = threading.Thread(target=self.receive)
        self.rcv.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name

    # to show chat window
        self.Window.deiconify()
        self.Window.title("Let's Chat")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#330000")
        self.labelHead = Label(self.Window,
                               bg="#330000",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#000000")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#330000",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#330000",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#330022",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

    # create a Send Button
        self.buttonImg = PhotoImage(file=r"greentick.png")
        self.buttonMsg = Button(self.labelBottom,
                                text="SEND ",
                                font="Helvetica 14 bold",
                                width=18,
                                bg="Navy Blue", fg="#00ff00",
                                image=self.buttonImg, compound=RIGHT,
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.Window.bind(
            '<Return>', lambda e: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

    # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

    # place the scroll bar
    # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

#function to exit the GUI interface
    def EXIT(self):
        if messagebox.askquestion("Quit","Are you sure to quit??") == "yes":
            self.client.close()
            self.Window.destroy()

# function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        self.snd = threading.Thread(target=self.sendMessage)
        self.snd.start()

# function to receive messages

    def receive(self):
        while not self.stop:
            try:
                message = self.client.recv(1024).decode(FORMAT)
            # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    self.client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                self.client.close()
                break


# function to send messages

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while not self.stop:
            time = datetime.datetime.now()
            time_msg = "%s/%s/%s-%s:%s:%s" % (time.day, time.month,
                                              time.year, time.hour, time.minute, time.second)
            message = (f"{self.msg}")
            self.client.send(time_msg.encode(FORMAT))
            self.client.send(message.encode(FORMAT))
            break


# create a GUI class object
g = GUI()
