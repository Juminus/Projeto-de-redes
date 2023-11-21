import tkinter as tk

class Tabuleiro:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Jogo do Tabuleiro")

        self.canvas = tk.Canvas(self.janela, width=400, height=400)
        self.canvas.pack()

        self.jogador1 = Jogador1(self)
        self.jogador2 = Jogador2(self, self.jogador1)

        self.rotulo_turno = tk.Label(self.janela, text="Turno: Jogador 1")
        self.rotulo_turno.pack()
        self.rotulo_jogadas = tk.Label(self.janela, text="Turnos restantes: 10")
        self.rotulo_jogadas.pack()
        self.contador_turnos = 10

        self.desenhar_tabuleiro()

        self.turno_atual = 1  # Inicia o turno com o jogador1
        self.movimentos_jogador1 = 0

    def desenhar_tabuleiro(self):
        # Desenhar tabuleiro
        for i in range(8):
            for j in range(8):
                cor = "white" if (i + j) % 2 == 0 else "grey"
                if i == 7 and j == 7:
                    cor = "green"
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=cor)

        # Desenhar barreiras
        for posicao in self.jogador2.barreiras:
            self.jogador2.desenhar_barreira(posicao)

        # Desenhar jogador
        self.jogador1.desenhar_jogador()

    def redesenhar_tabuleiro(self):
        # Limpar canvas
        self.canvas.delete("all")

        # Redesenhar tabuleiro
        self.desenhar_tabuleiro()

    def iniciar(self):
        self.proximo_turno()
        self.janela.mainloop()

    def proximo_turno(self):
        if self.turno_atual == 1:
            # Inicia o turno do jogador1
            self.turno_jogador1()
        elif self.turno_atual == 2:
            # Inicia o turno do jogador2
            self.turno_jogador2()

    def turno_jogador1(self):
    # Atualiza o título da janela para indicar o turno do jogador1
        self.rotulo_turno.config(text=f"Turno: Jogador 1")

        # Habilita os movimentos do jogador1
        self.janela.bind("<Key>", self.jogador1.mover_jogador)

    def turno_jogador2(self):
        self.rotulo_turno.config(text=f"Turno: Jogador 2")

        # Habilita a colocação de barreiras pelo jogador2
        self.janela.bind("<Button-1>", self.jogador2.colocar_barreira)


    def finalizar_turno(self):
        if self.turno_atual == 1:
            self.movimentos_jogador1 += 1
            if self.movimentos_jogador1 >= 2:
                # Se o jogador1 fez 2 movimentos, passa para o turno do jogador2
                self.turno_atual = 2
                self.janela.unbind("<Key>")
                self.janela.after(100, self.turno_jogador2())
        elif self.turno_atual == 2:
            # Se o jogador2 colocou a barreira, passa para o turno do jogador1
            self.movimentos_jogador1 = -1
            self.turno_atual = 1
            self.janela.unbind("<Button-1>")
            self.janela.after(100, self.turno_jogador1())
            self.contador_turnos -=1
            self.rotulo_jogadas.config(text=f"Jogadas restantes: {self.contador_turnos}")
            self.finalizar_turno()
         # Verifica se o jogador2 atingiu 10 jogadas para vencer
        if self.contador_turnos == 0:
            print("Jogador 2 é o vencedor!")
            self.janela.destroy()


class Jogador1:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro
        self.posicao = (0, 0)
        self.canvas = self.tabuleiro.canvas

    def desenhar_jogador(self):
        x, y = self.posicao
        self.jogador_id = self.canvas.create_oval(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="blue")

    def mover_jogador(self, event):
        x, y = self.posicao

        if event.char == "w" and y > 0 and not self.verificar_barreira((x, y - 1)):
            y -= 1
            self.tabuleiro.finalizar_turno()

        elif event.char == "a" and x > 0 and not self.verificar_barreira((x - 1, y)):
            x -= 1
            self.tabuleiro.finalizar_turno()

        elif event.char == "s" and y < 7 and not self.verificar_barreira((x, y + 1)):
            y += 1
            self.tabuleiro.finalizar_turno()

        elif event.char == "d" and x < 7 and not self.verificar_barreira((x + 1, y)):
            x += 1
            self.tabuleiro.finalizar_turno()

        nova_posicao = (x, y)
        self.atualizar_posicao(nova_posicao)
        self.verificar_objetivo()

    def verificar_barreira(self, posicao):
        return posicao in self.tabuleiro.jogador2.barreiras

    def atualizar_posicao(self, nova_posicao):
        self.posicao = nova_posicao
        self.tabuleiro.redesenhar_tabuleiro()

    def verificar_objetivo(self):
        if self.posicao == (7, 7):
            print("Parabéns! Você alcançou a posição final.")
            self.tabuleiro.janela.destroy()


class Jogador2:
    def __init__(self, tabuleiro, jogador1):
        self.tabuleiro = tabuleiro
        self.jogador1 = jogador1
        self.barreiras = []  # Lista para armazenar as posições das barreiras
        self.barreiras_limit = 3
        self.canvas = self.tabuleiro.canvas
        self.barreira_atual = 0  # Índice da barreira a ser removida ao atingir o limite

    def desenhar_barreira(self, posicao):
        x, y = posicao
        self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="red", tags="barreiras")

    def remover_barreira(self, posicao):
        x, y = posicao
        cor = "white" if (x + y) % 2 == 0 else "grey"
        self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=cor)

    def colocar_barreira(self, event):
        if len(self.barreiras) < self.barreiras_limit:
            x = event.x // 50
            y = event.y // 50
            posicao = (x, y)

            # Verifica se a posição é válida e não é a posição final do jogador1
            if (
                posicao not in self.barreiras
                and posicao != (7, 7)
                and posicao != self.jogador1.posicao
            ):
                self.barreiras.append(posicao)
                self.desenhar_barreira(posicao)

                # Se ultrapassou o limite, remove a primeira barreira
                if len(self.barreiras) == self.barreiras_limit:
                    posicao_remover = self.barreiras.pop(0)
                    self.remover_barreira(posicao_remover)
                
                self.tabuleiro.finalizar_turno()

            elif len(self.barreiras) == self.barreiras_limit:
                # Se ultrapassou o limite, mas a posição clicada é a posição final do jogador1,
                # então não faz nada
                pass
            elif posicao == (7, 7):
                # Se a posição clicada é a posição final do jogador1, então não faz nada
                pass


class Main:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.tabuleiro.iniciar()

if __name__ == "__main__":
    jogo = Main()
