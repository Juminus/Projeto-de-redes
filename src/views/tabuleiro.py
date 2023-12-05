import tkinter as tk
from tkinter import messagebox
import threading
import json

from src.models.jogador1 import Jogador1
from src.models.jogador2 import Jogador2
from src.settings import settings

class Tabuleiro:
    def __init__(self, root, client_socket):
        try:
            self.root = root
            self.client_socket = client_socket
            self.widgets = {}
            self.gameover = False
            self.desenhar_tabuleiro()

        except Exception as e:
            print("init_tabuleiro:", e)


    def conectar_server(self):
        try:
            self.client_socket.connect((settings.HOST, settings.PORT))
            threading._start_new_thread(self.tratar_mensagem, (self.client_socket, "m"))

        except Exception as e:
            print("conect_server:",e)


    def tratar_mensagem(self, socket, m):
        while True:
                msg = socket.recv(settings.TAM_BUFFER)
                msg_servidor = json.loads(msg.decode())
                if not msg_servidor:
                    return
                
                elif msg_servidor["head"] == "bem_vindo":
                    self.username = msg_servidor["body"]
                    self.widgets["status"]["label"].config(text="Aguardando Jogador2...")
                    self.widgets["bottom_status"]["label"].pack()
                    self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}".title())
                    self.widgets["connect"]["frame"].pack_forget()

                elif msg_servidor["head"] == "contagem_regressiva":
                    self.widgets["status"]["label"].config(text=msg_servidor["body"])

                elif msg_servidor["head"] == "sua_vez":
                    self.widgets["status"]["label"].config(text="Seu turno! ")
                    self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}".title())
                    self.fazer_jogada()

                elif msg_servidor["head"] == "adversario":
                        self.widgets["status"]["label"].config(text="Turno do adversário! ")
                        self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}".title())

                elif msg_servidor["head"] == "jogada":
                    self.receber_jogada(msg_servidor["from"], msg_servidor["body"])

                elif msg_servidor["head"] == "fim_de_jogo":
                    self.fim_de_jogo(msg_servidor["body"])


    def enviar_comando(self, role, action, args):
        try:
            comando = {"from": role, "head": action, "body": args}
            self.client_socket.sendall(json.dumps(comando).encode("UTF-8"))

        except Exception as e:
            print("enviar_comando:",e)


    def desenhar_tabuleiro(self):
        try:
            self.status_bar = tk.Frame(self.root)
            self.janela = tk.Frame(self.root)
            self.connect_bar = tk.Frame(self.status_bar)
            self.bottom_status_bar = tk.Frame(self.root)

            self.status_label = tk.Label(
                self.status_bar,
                text="Aguardando jogadores...",
                pady=10,
                font=("Arial", 15),
            )
            self.status_label.pack()

            self.canvas = tk.Canvas(self.janela, width=400, height=400)
            self.canvas.pack()

            self.p1 = Jogador1(self)
            self.p2 = Jogador2(self, self.p1)

            for i in range(8):
                for j in range(8):
                    cor = "white" if (i + j) % 2 == 0 else "grey"
                    if i == 7 and j == 7:
                        cor = "green"
                    self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=cor)

            for posicao in self.p2.barreiras:
                self.p2.desenhar_barreira(posicao)

            self.p1.desenhar_jogador()
            
            self.connect_button = tk.Button(self.connect_bar, text="Conectar")
            self.connect_button.bind("<Button-1>", lambda event, button=self.connect_button: self.conectar_server())
            self.connect_button.pack()
            self.connect_bar.pack()

            self.bottom_status_label = tk.Label(
                self.bottom_status_bar,
                text="",
                pady=10,
                font=("Arial", 15),
            )

            self.widgets["status"] = {"frame": self.status_bar, "label": self.status_label}
            self.widgets["board"] = {"frame": self.janela, "canvas": self.canvas}
            self.widgets["connect"] = {"frame": self.connect_bar, "button": self.connect_button}
            self.widgets["bottom_status"] = {
                "frame": self.bottom_status_bar,
                "label": self.bottom_status_label,
            }

            self.status_bar.grid(row=0)
            self.janela.grid(row=1)
            self.bottom_status_bar.grid(row=2)

        except Exception as e:
            print("desenhar_tabuleiro:",e)


    def fim_de_jogo(self, vencedor):
        messagebox.showinfo("PeBa", vencedor)
        self.root.destroy()


    def fazer_jogada(self):
        try:
            if self.username == "jogador1":
                self.widgets["status"]["label"].config(text="Sua vez!")
                self.root.bind("<KeyPress>", self.p1.mover_jogador)

            elif self.username == "jogador2":
                self.widgets["status"]["label"].config(text="Sua vez!")
                self.root.bind("<Button-1>", self.p2.colocar_barreira)
            return

        except Exception as e:
            print("fazer jogada:", e)


    def receber_jogada(self, role, movimento):
        try:
            if role == "jogador2":
                self.p2.atualizar_barreira(movimento)

            elif role == "jogador1":
                self.p1.atualizar_posicao(movimento)

        except Exception as e:
            print("ReceberJogada:", e)
            print(role)
            print(movimento)
