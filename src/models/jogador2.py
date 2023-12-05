class Jogador2:
    def __init__(self, tabuleiro, jogador1):
        self.tabuleiro = tabuleiro
        self.jogador1 = jogador1
        self.barreiras = []  # Lista para armazenar as posições das barreiras
        self.barreiras_limit = 3
        self.canvas = self.tabuleiro.canvas
        self.barreira_atual = 0  # Índice da barreira a ser removida ao atingir o limite
        self.contador_turnos = 12


    def desenhar_barreira(self, posicao):
        x, y = posicao
        self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="red", tags="barreiras")


    def remover_barreira(self, posicao):
        x, y = posicao
        cor = "white" if (x + y) % 2 == 0 else "grey"
        self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=cor)


    def colocar_barreira(self, event):
        self.tabuleiro.root.unbind("<Button-1>")

        if len(self.barreiras) < self.barreiras_limit:
            x = event.x // 50
            y = event.y // 50
            posicao = [x, y]

            if (
                posicao not in self.barreiras
                and posicao != [7, 7]
                and posicao != self.jogador1.posicao
            ):
                self.barreiras.append(posicao)
                self.desenhar_barreira(posicao)

                # Se ultrapassou o limite, remove a primeira barreira
                if len(self.barreiras) == self.barreiras_limit:
                    posicao_remover = self.barreiras.pop(0)
                    self.remover_barreira(posicao_remover)
                self.contabiliza_turnos()
                self.tabuleiro.enviar_comando("jogador2", "jogada", posicao)

            else:
                self.tabuleiro.fazer_jogada()


    def atualizar_barreira(self, posicao):
        self.barreiras.append(posicao)
        self.contabiliza_turnos()
        self.desenhar_barreira(posicao)

        if len(self.barreiras) == self.barreiras_limit:
            posicao_remover = self.barreiras.pop(0)
            self.remover_barreira(posicao_remover)
            

    def contabiliza_turnos(self):
        self.contador_turnos -= 1
        if self.contador_turnos == 0:
            self.tabuleiro.enviar_comando("jogador2", "fim_de_jogo", "O Jogador2 é o vencedor!")
            self.tabuleiro.fim_de_jogo("O Jogador2 é o vencedor!")


