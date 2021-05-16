from file_func import Client_Connect, Write_New
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
class Server:

    HOST = ''
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    connections = {}
    addresses = {}

    def __init__(self):
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(Server.ADDR)
        self.SERVER.listen(10)
        self.connectionLoop = Thread(
            target=Server.client_request_thread, args=(self,))
        self.connectionLoop.start()
        self.connectionLoop.join()
        self.SERVER.close()

    def client_request_thread(self):
        """Sets up handling for incoming clients."""
        print("Server started")
        while True:
            client, client_address = self.SERVER.accept()
            print("Client Connected : ", client_address)
            Server.addresses[client] = client_address
            client.send(Client_Connect().encode("utf8"))
            Thread(target=Server.client_thread, args=(self, client,)).start()

    def client_thread(self, client):
        client.send(bytes('NAME', "utf8"))
        name = client.recv(Server.BUFSIZ).decode("utf8")
        Server.connections[client] = name
        while True:
            time= client.recv(Server.BUFSIZ).decode("utf8")
            msg = client.recv(Server.BUFSIZ).decode("utf8")
            if msg != "bye":
                Server.broadcast(msg,"{Time}=>\t{Name}:\t".format(Time=time,Name=name))
                Write_New(time,name,msg)
            else:
                client.send(bytes("bye", "utf8"))
                client.close()
                del Server.connections[client]
                break

    def broadcast(msg, prefix=""): 
        for sock in Server.connections:
            sock.send(bytes(prefix + msg, "utf8"))


s = Server()
