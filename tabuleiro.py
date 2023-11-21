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
