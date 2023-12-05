class Jogador1:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro
        self.posicao = [0, 0]
        self.canvas = self.tabuleiro.canvas
        self.ultimaJogada = ""
        self.num_jogadas = 0


    def desenhar_jogador(self):
        x, y = self.posicao
        self.jogador_id = self.canvas.create_oval(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="blue")


    def mover_jogador(self, event):
        self.tabuleiro.root.unbind("<KeyPress>")

        if (self.num_jogadas % 2) == 0:
            self.ultimaJogada = ""

        x, y = self.posicao

        if event.char == "w" and y > 0 and not self.verificar_barreira([x, y - 1]) and self.ultimaJogada != "s":
            y -= 1
            self.ultimaJogada = "w"
            self.movimento_valido(x, y)

        elif event.char == "a" and x > 0 and not self.verificar_barreira([x - 1, y]) and self.ultimaJogada != "d":
            x -= 1
            self.ultimaJogada = "a"
            self.movimento_valido(x, y)

            
        elif event.char == "s" and y < 7 and not self.verificar_barreira([x, y + 1]) and self.ultimaJogada != "w":
            y += 1
            self.ultimaJogada = "s"
            self.movimento_valido(x, y)


        elif event.char == "d" and x < 7 and not self.verificar_barreira([x + 1, y]) and self.ultimaJogada != "a":
            x += 1
            self.ultimaJogada = "d"
            self.movimento_valido(x, y)
        
        else:
            self.tabuleiro.fazer_jogada()


    def movimento_valido(self, x, y):
        self.nova_posicao = [x, y]
        self.atualizar_posicao(self.nova_posicao)
        self.verificar_objetivo()
        self.num_jogadas += 1
        self.tabuleiro.enviar_comando("jogador1", "jogada", self.nova_posicao)


    def verificar_barreira(self, posicao):
        return posicao in self.tabuleiro.p2.barreiras


    def atualizar_posicao(self, nova_posicao):
        x, y = nova_posicao
        self.x1, self.y1 = self.posicao
        self.cor = "white" if (self.x1 + self.y1) % 2 == 0 else "grey"
        self.canvas.create_rectangle(self.x1 * 50, self.y1 * 50, (self.x1 + 1) * 50, (self.y1 + 1) * 50, fill=self.cor)
        self.jogador_id = self.canvas.create_oval(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="blue")
        self.posicao = nova_posicao


    def verificar_objetivo(self):
        if self.posicao == [7, 7]:
            self.tabuleiro.enviar_comando("jogador1", "fim_de_jogo", "O Jogador1 é o vencedor!")
            self.tabuleiro.fim_de_jogo("O Jogador1 é o vencedor!")