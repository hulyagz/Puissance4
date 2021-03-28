import socket
import signal
import sys #utilisé pour sortir du programme
import time
from clientThread import ClientListener

class Server():

    def __init__(self, port):
        self.client_sockets = None
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets = []
        self.currentPlayer = 0
        self.player = 1
        self.player2 = 2
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signal, frame):
        print(signal)
        self.listener.close()
        self.echo("QUIT")
        
    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)
            
    def remove_socket(self, socket):
        self.client_sockets.remove(socket)

    def echo(self, data):
        print("echoing:", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")
                    
server=Server(59001)
server.run()
