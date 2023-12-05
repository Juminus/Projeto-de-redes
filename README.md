# Documentação PeBa
<h1 align = 'center'>Introdução</h1>
<p>Este projeto consiste em um jogo de tabuleiro multiplayer implementado em Python, onde dois jogadores competem por 12 turnos. A comunicação entre os jogadores é realizada por meio de sockets TCP, garantindo uma transmissão confiável de dados.</p>

<h1 align = 'center'>Funcionamento do Jogo</h1>
<p>O jogo é baseado em turnos, com o Jogador 1 realizando duas movimentações consecutivas, seguido pelo Jogador 2, que coloca uma barreira. Esse ciclo se repete por 12 turnos. O objetivo do Jogador 1 é atingir seu destino, enquanto o Jogador 2 busca impedir seu progresso com barreiras estratégicas.</p>

<h1 align = 'center'>Protocolo de Comunicação</h1>
<h2>1. Eventos</h2>
As trocas de informações, cliente e servidor, são feitas através de arquivo JSON estruturados da seguinte forma:<br>

```python
def estruturar_comando(role="", action="", args=""):
    try:
        comando = {"from": role, "head": action, "body": args}
        return json.dumps(comando).encode("UTF-8")
    
    except Exception as e:
            print("estruturar_comando_server:", e)
```

Seguem os eventos: <br>

- Vez do jogador (sua_vez) 
- Emissor: Servidor 
- Receptor: Jogador (Jogador 1 ou Jogador 2)
- Descrição: Indica que é a vez do jogador realizar uma ação (movimento ou colocação de barreira).<br>
Código exemplo:
```python
elif msg_servidor["head"] == "sua_vez":
                    print("fazer jogada: ", msg_servidor)
                    self.widgets["status"]["label"].config(text="Seu turno! ")
                    self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}")
                    self.fazer_jogada()
```
Código de tratamento de mensagem:
```python
mensagem = estruturar_comando("servidor", "sua_vez", "jogador1")
p1.socket.sendall(mensagem)
mensagem = estruturar_comando("servidor", "sua_vez", "jogador2")
p2.socket.sendall(mensagem)
```


- Vez do adversário (adversario) 
- Emissor: Servidor.
- Receptor: Jogador (Jogador 1 ou Jogador 2).
- Descrição: Este trecho de código é acionado quando o servidor envia uma mensagem com o cabeçalho "adversario". Quando isso ocorre, o código imprime uma mensagem no console indicando que é a vez do jogador adversário realizar uma jogada. Além disso, ele atualiza a interface do usuário para refletir essa informação.<br>


<p>Codigo...</p>

<h2>2. Estados</h2>

<p>Turno Atual<br>

Valores: 0 (Jogador 1) ou 1 (Jogador 2)<br>
Descrição: Define qual jogador deve realizar a próxima ação.<br>
Exemplo no código:</p>

<h2> 3 - Mensagens</h2>

Bem-Vindo (bem_vindo)<br>
- Emissor: Servidor<br>
- Receptor: Jogador<br>
- Descrição: Saudação ao jogador, informando qual é o seu papel no jogo.<br>
Exemplo no código:

<p>Contagem Regressiva (contagem_regressiva)<br>

Emissor: Servidor<br>
Receptor: Jogadores<br>
Descrição: Informa aos jogadores que o jogo começará em breve, contando regressivamente.<br>
Exemplo no código:</p>

<h1>Estruturação e organização do projeto</h1>

|--src<br>
|-----models<br>
|-----------jogador.py<br>
|-----------jogador1.py<br>
|-----------jogador2.py<br>
|-----settings<br>
|-----------setting.py<br>
|-----views<br>
|----------tabuleiro.py<br>
|-----client.py<br>
|-----server.py<br>

Descrição:<br>

src - Pasta pai do projeto<br>
models - Pasta filha de src, onde se localiza as classes de jogadores<br>
`jogador.py` - Classe para inicialização do jogador na rede<br>
`jogador1.py` - Classe onde se encontra as funcionalidades do jogador 1<br>
`jogador2.py` - Classe onde se encontra as funcionalidades do jogador 2<br>
settings - Pasta filha de src, onde é guardada a classe settings.py<br>
`settings.py` - Classe onde se armazena o ip e a porta <br>
views - Pasta filha de src, onde se localiza o jogo
`tabuleiro.py` - Onde se localiza as funcionalidades do jogo
`client.py`- Classe responsável pela conexão do jogador com o jogo. Necessária para a interação dos jogadores com o jogo
`server.py` - Classe que inicia um servidor para o recebimento e envio de comandos

<h1 align = 'center'>Motivação da escolha do protocolo de transporte </h1>
<p>O uso do protocolo TCP na implementação deste jogo de tabuleiro multiplayer em Python foi uma escolha estratégica fundamentada em diversos critérios. O protocolo TCP oferece uma série de características essenciais que se alinham perfeitamente com as necessidades específicas deste ambiente de jogo.
</p>

<h2>-Confiabilidade na Entrega de Dados:</h2>
<p>O protocolo TCP garante a entrega confiável de dados entre o cliente e o servidor. Isso é crucial para garantir que todas as movimentações dos jogadores e a colocação de barreiras sejam recebidas e processadas corretamente, sem perda de informações durante a transmissão.</p>

<h2>-Ordem de Entrega:</h2>
<p>A ordem em que as mensagens são enviadas e recebidas é preservada pelo TCP. Em um jogo com turnos definidos, como é o caso aqui, manter a ordem correta das ações é vital para garantir a sincronização entre os jogadores, assegurando uma experiência de jogo coesa.</p>

<h2>-Controle de Congestionamento:</h2>
<p>O TCP incorpora mecanismos eficientes de controle de congestionamento, evitando sobrecargas na rede. Isso é crucial para garantir um desempenho estável do jogo, mesmo em condições de tráfego intenso na rede.</p>

<h2>-Segurança na Comunicação:</h2>
<p>O TCP fornece um nível adicional de segurança, garantindo que os dados transmitidos entre o cliente e o servidor não sejam comprometidos durante a transferência. Isso é crucial para impedir manipulações indesejadas que poderiam afetar a integridade do jogo.</p>

<p>Em resumo, a escolha do protocolo TCP para a comunicação entre o cliente e o servidor neste jogo de tabuleiro multiplayer em Python é fundamentada na busca por uma comunicação robusta, confiável e ordenada, elementos cruciais para garantir uma experiência de jogo fluida e sem contratempos para os jogadores envolvidos.</p>

<h1 align = 'center'>Funcionamento do Software</h1>
<p></p>

<h1 align = 'center'>Propósito do Software</h1>
<p>É um projeto da matéria de redes do curso de Ciência da Computação que tem o propósito de fornecer uma experiência de jogo interativa e desafiadora para dois jogadores, envolvendo estratégia. O jogo busca proporcionar diversão enquanto promove a competição amigável entre os participantes.</p>

<h1 align = 'center'>Requisitos Mínimos</h1>
<p>Uma computador com sistema operacional Linux ou Windowns</p>
<p>Python 3 instalado</p>
<p>Conexão de rede entre os jogadores</p>
<p>Capacidade de executar sockets TCP</p>

<h1 align = 'center'>Conclusão</h1>
<p>Este jogo de tabuleiro multiplayer em Python oferece uma experiência dinâmica e estratégica, facilitada pela comunicação eficiente proporcionada pelo protocolo TCP. A documentação do protocolo e do software visa facilitar o entendimento e aprimoramento contínuo deste projeto. Divirta-se jogando!
</p>
