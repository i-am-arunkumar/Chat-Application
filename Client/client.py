from socket import AF_INET, SOCK_STREAM, socket
from tkinter import *
import threading
import tkinter.messagebox

FORMAT = 'utf8'

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)


class GUI:
    # constructor method
    """def buttonClick(self):
             if(self.entryPass.get() == "1234"):
                self.goAhead(self.entryName.get())
             else:
                tkinter.messagebox.showerror("ERROR","WRONG PASSWORD, TRY AGAIN")"""
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
        self.login.configure(bg="#ffcc99")
        # create a Label
        self.pls = Label(self.login,
                         text="LET'S CHAT!\n Enter Name To Continue:",
                         justify=CENTER,
                         font="Times 16 bold", bg="#ffcc99")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)


        self.labelName = Label(self.login,
                               text="NAME:",
                               font="Times 14 bold", bg="#ffcc99")

        self.labelName.place(relheight=0.1,
                             relx=0.1,
                             rely=0.4)

        self.icon = PhotoImage(file= r"C:\Users\Lenovo\Desktop\chat.png")
        self.iconLabel = Label(self.login, image=self.icon,bg="#ffcc99")
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
        """self.entryPass = Entry(self.login)

        self.entryPass.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.45,
                             rely=0.40)

        self.entryPass.focus()"""

        # create a Continue Button
        # along with action

        self.go = Button(self.login,
                         text="LOGIN",
                         font="Times 14 bold", bg="light blue",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.flash()

        self.go.place(relx=0.4,
                      rely=0.60)



        self.Window.mainloop()


    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        self.client = socket(AF_INET, SOCK_STREAM)
        print(ADDR)
        self.client.connect(ADDR)
        rcv = threading.Thread(target=self.receive)
        rcv.start()

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
                          bg="#ffcc99")
        self.labelHead = Label(self.Window,
                           bg="light blue",
                           fg="#001a4d",
                           text=self.name,
                           font="Times 13 bold",
                           pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                      width=450,
                      bg="light blue")

        self.line.place(relwidth=1,
                    rely=0.07,
                    relheight=0.012)

        self.textCons = Text(self.Window,
                         width=20,
                         height=2,
                         bg="#ffcc99",
                         fg="black",
                         font="Times 14 bold",
                         padx=5,
                         pady=5)

        self.textCons.place(relheight=0.745,
                        relwidth=1,
                        rely=0.175)

        self.labelBottom = Label(self.Window,
                             bg="light blue",
                             height=80)

        self.labelBottom.place(relwidth=1,
                           rely=0.9)

        self.entryMsg = Entry(self.labelBottom,
                          bg="#ffcc99",
                          fg="black",
                          font="Times 13")

    # place the given widget
    # into the gui window
        self.entryMsg.place(relwidth=0.74,
                        relheight=0.03,
                        rely=0.008,
                        relx=0.011)

        self.entryMsg.focus()

    # create a Send Button
        self.buttonImg = PhotoImage(file = r"C:\Users\Lenovo\Desktop\greentick.png")
        self.buttonMsg = Button(self.labelBottom,
                            text="SEND",
                            font="Times 14 bold",
                            width=18,
                            bg="#00ff00", image = self.buttonImg,compound = RIGHT,
                            command=lambda: self.sendButton(self.entryMsg.get()))

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


# function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()


# function to receive messages
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(FORMAT)
                print(message)
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
        while True:
            message = (f"{self.msg}")
            self.client.send(message.encode(FORMAT))
            break


# create a GUI class object
g = GUI()
