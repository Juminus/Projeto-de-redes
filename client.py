import socket
import tkinter as tk

from src.views.tabuleiro import Tabuleiro

client_socket = socket.socket()

root = tk.Tk()
root.title("PeBa")

gi = Tabuleiro(root, client_socket)

root.mainloop()
