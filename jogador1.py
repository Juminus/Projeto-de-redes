
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
