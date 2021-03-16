import tkinter as tk
from tkinter import *

import P4
from client import Client
from tkinter import scrolledtext


class ClientApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=2)

        self.frames = {}
        for F in (StartPage, PageMain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Messagerie config:", fg="blue").grid(row=0, column=0)
        tk.Label(self, text="username:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="server:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="port:").grid(row=3, column=0, padx=10, pady=10)

        self.entryUsername = tk.Entry(self)
        self.entryUsername.grid(row=1, column=1)
        self.entryServer = tk.Entry(self)
        self.entryServer.grid(row=2, column=1)
        self.entryPort = tk.Entry(self)
        self.entryPort.grid(row=3, column=1)
        button = tk.Button(self, text="valider", width=20, fg="blue", command=lambda: self.validateConfig({
            'username': self.entryUsername.get(),
            'server': self.entryServer.get(),
            'port': int(self.entryPort.get())
        }))
        button.place(relx=0.5, rely=0.5, anchor=CENTER)
        button.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

    def validateConfig(self, data):
        self.controller.frames['PageMain'].receive_data(data)
        self.controller.show_frame("PageMain")


class PageMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.messages = scrolledtext.ScrolledText(self, width=50)
        self.messages.grid(row=0, column=0, padx=10, pady=10)

        self.entryMessage = tk.Entry(self, width=30)
        self.entryMessage.insert(0, "Votre message")
        self.entryMessage.grid(row=1, column=0, padx=10, pady=10)
        self.messages.tag_config('message', foreground='#3498db')

        def send_message():
            clientMessage = self.entryMessage.get()
            self.client.send(clientMessage)

        btnSendMessage = tk.Button(self, text="Send", width=20, command=send_message)
        btnSendMessage.grid(row=2, column=0, padx=10, pady=20)

    #can = Canvas()
    #can.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

    def receive_data(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.client.listen(self.handle)

    def handle(self, data):
        self.messages.insert(tk.END, data + '\n', 'message')


if __name__ == '__main__':
    ClientApp().mainloop()
