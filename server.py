import threading
import socket
import json
import time

from src.models.jogador import Jogador
from src.settings import settings

def estruturar_comando(role="", action="", args=""):
    try:
        comando = {"from": role, "head": action, "body": args}
        return json.dumps(comando).encode("UTF-8")
    
    except Exception as e:
            print("estruturar_comando_server:", e)


def tratar_mensagem(client_socket, m):
    global turno
    try:
        while True:
            if turno == 0 or turno == 1:
                mensagem = json.loads(p1.socket.recv(settings.TAM_BUFFER).decode())

                if turno == 0:
                    passa_turno_jogar1()

                elif turno == 1:
                    passa_turno_jogar2()

                turno += 1
                     
            elif turno == 2:
                mensagem = json.loads(p2.socket.recv(settings.TAM_BUFFER).decode())
                turno = 0
                passa_turno_jogar1()

            if not mensagem:
                return

            if mensagem["head"] == "jogada":
                if mensagem["from"] == "jogador1":
                        p2.socket.sendall(json.dumps(mensagem).encode("UTF-8"))

                elif mensagem["from"] == "jogador2":
                        p1.socket.sendall(json.dumps(mensagem).encode("UTF-8"))
                    
            elif mensagem["head"] == "fim_de_jogo":
                if mensagem["from"] == "jogador1":
                        p2.socket.sendall(json.dumps(mensagem).encode("UTF-8"))

                elif mensagem["from"] == "jogador2":
                        p1.socket.sendall(json.dumps(mensagem).encode("UTF-8"))

    except Exception as e:
            print("Tratar_mensagem_server:", e)


def passa_turno_jogar1():
    mensagem = estruturar_comando("servidor", "sua_vez", "jogador1")
    p1.socket.sendall(mensagem)

    mensagem = estruturar_comando("servidor", "adversario")
    p2.socket.sendall(mensagem)


def passa_turno_jogar2():
    mensagem = estruturar_comando("servidor", "sua_vez", "jogador2")
    p2.socket.sendall(mensagem)

    mensagem = estruturar_comando("servidor", "adversario")
    p1.socket.sendall(mensagem)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((settings.HOST, settings.PORT))
    
except:
    print('\nNão foi possível iniciar o servidor!\n')

server.listen()

clients = []
turno = 0


try:
    while len(clients) < 2:
        print(f'Esperando conexão: {len(clients)}/2')
        client_socket, cliente_addr = server.accept()
        novo_jogador = Jogador(cliente_addr, client_socket, settings.ROLES.pop())
        clients.append(novo_jogador)
        jogador_role = novo_jogador.role["role"]

        bem_vindo = estruturar_comando("servidor", "bem_vindo", jogador_role)
        client_socket.sendall(bem_vindo)
    print(f'Esperando conexão: {len(clients)}/2')
    print(f'Conectado!')
    
    p1 = clients[0]
    p2 = clients[1]

    threading._start_new_thread(tratar_mensagem, (p1.socket, "m"))
    threading._start_new_thread(tratar_mensagem, (p2.socket, "m"))

    for count in range(3, 0, -1):
        cont_regressiv = estruturar_comando("servidor", "contagem_regressiva", f"O jogo vai começar em \n {count} \n segundo(s)!")
        p2.socket.sendall(cont_regressiv)
        p1.socket.sendall(cont_regressiv)
        time.sleep(1)
        if count == 0:
            break

    mensagem = estruturar_comando("servidor", "sua_vez", "jogador1")
    p1.socket.sendall(mensagem)    
    mensagem = estruturar_comando("servidor", "adversario")
    p2.socket.sendall(mensagem)

except Exception as e:
        print("main:",e)

jogando = True
while jogando:
    pass