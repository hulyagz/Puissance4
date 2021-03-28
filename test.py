from tkinter import *
import tkinter as tk
from tkinter import scrolledtext


root = tk.Tk.Frame()
root.title('test')
root.geometry('1000x600')
monCanvas = Canvas(root, width=500, height=500, bg='ivory')

monCanvas.grid(row=0, column=0)
message = scrolledtext.ScrolledText(width=50)
message.grid(row=0, column=1)
entryMessage = Entry(width=30)
entryMessage.insert(0, "Votre message")
entryMessage.grid(row=1, column=1, padx=10, pady=10)
message.tag_config('message', foreground='#3498db')

if __name__ == "__main__":
    mainloop()

