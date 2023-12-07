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

### Evento "Bem vindo":

- Tela de espera pelo jogador 2 (`bem_vindo`) 
- Emissor: Servidor 
- Receptor: Jogador 1
- Descrição: Indica que após o jogador 1 clicar em conectar aparecerá em sua tela uma mensagem falando que o servidor está a espera o jogador 2 se conectar. Essa mensagem só desaparece depois depois que o jogador 2 se conectar.<br>

Código:
```python
elif msg_servidor["head"] == "bem_vindo":
                    self.username = msg_servidor["body"]
                    self.widgets["status"]["label"].config(text="Aguardando Jogador2...")
                    self.widgets["bottom_status"]["label"].pack()
                    self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}".title())
                    self.widgets["connect"]["frame"].pack_forget()
```


### Evento "sua vez":

- Vez do jogador (`sua_vez`) 
- Emissor: Servidor 
- Receptor: Jogador (Jogador 1 ou Jogador 2)
- Descrição: Indica que é a vez do jogador realizar uma ação (movimento ou colocação de barreira).<br>
Código:
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

### Evento "adversário":

- Vez do adversário (`adversario`) 
- Emissor: Servidor.
- Receptor: Jogador (Jogador 1 ou Jogador 2).
- Descrição: Este trecho de código é acionado quando o servidor envia uma mensagem com o cabeçalho "adversario". Quando isso ocorre, o código imprime uma mensagem no console indicando que é a vez do jogador adversário realizar uma jogada. Além disso, ele atualiza a interface do usuário para refletir essa informação.<br>
Código:
```python
elif msg_servidor["head"] == "adversario":
                        self.widgets["status"]["label"].config(text="Turno do adversário! ")
                        self.widgets["bottom_status"]["label"].config(text=f"{self.username} | Turnos Restantes: {self.p2.contador_turnos}".title())
```

### Evento "Contagem regressiva":

- Contagem Regressiva (`contagem_regressiva`): Faz uma contagem regressiva de 3 a 1 para o inicío do jogo.
- Emissor: Servidor
- Receptor: Jogador (Jogador 1 ou Jogador 2).
- Descrição: Esta mensagem é enviada pelo servidor para informar aos jogadores que a partida irá começar depois daquela contagem, para que ambos tenha noção do início do jogo.<br>
Código:
```python
elif msg_servidor["head"] == "contagem_regressiva":
                    self.widgets["status"]["label"].config(text=msg_servidor["body"])
```

### Evento "Jogada":
- Jogada (`jogada`): Indica que algum jogador fez uma jogada.
- Emissor: Servidor
- Receptor: Jogador (Jogador 1 ou Jogador 2).
- Descrição: O servidor envia uma mensagem indicando uma jogada realizada por um dos jogadores. O código chama a função `receber_jogada` para processar e aplicar a jogada recebida.<br>
Código:
```python
elif msg_servidor["head"] == "jogada":
                    self.receber_jogada(msg_servidor["from"], msg_servidor["body"])
```

### Evento "Fim de jogo":
- Final do jogo (`jogada`): Faz uma contagem regressiva de 3 a 1 para o inicío do jogo.
- Emissor: Servidor
- Receptor: Jogador (Jogador 1 ou Jogador 2).
- Descrição: O servidor envia uma mensagem indicando uma jogada realizada por um dos jogadores. O código chama a função `receber_jogada` para processar e aplicar a jogada recebida.<br>
Código:
```python
elif msg_servidor["head"] == "fim_de_jogo":
                    self.fim_de_jogo(msg_servidor["body"])
```


<h2>2. Estados</h2>

### O jogo é composto por alguns estados, sendo eles:<br>

- Inicialização do tabuleiro: <br>
Descrição: O jogo inicia com o tabuleiro e uma mensagem falando que está aguardando os jogadores.

- Aguardando jogador 2: <br>
Descrição: O estado é acionado após o jogador 1 clicar em conectar.

- Contagem regressiva após o jogador 2 se conectar:<br>
Descrição: Após o jogador 2 apertar em conectar, irá aparecer uma contagem regressiva de 3 segundos para o início do jogo.

- Vez do jogador1 :<br>
Descrição: O jogador 1 é o primeiro a jogar, se movimentando pelo tabuleiro, e joga novamente após o jogador 2 colocar uma barreira.<br>

- Vez do jogador2 :<br>
Descrição: O jogador 2 é o segundo a jogar, colocando barreiras, e joga após o jogador 1 se movimentar duas vezes.<br>

<h2> 3 - Mensagens</h2>

### 1 - Mensagens do Cliente para o Servidor:

- Conexão Inicial:<br>
Mensagem: Conectar ao Servidor<br>
Método: `self.conectar_server()`<br>

- Mensagens de Jogo:<br>
Mensagem: Enviar Comando para o Servidor<br>
Método: self.enviar_comando(role, action, args)

### 2 - Mensagens do Servidor para o Cliente:

- Bem-vindo:<br>
Mensagem: Bem-vindo ao Jogo<br>
Head: bem_vindo<br>

- Contagem Regressiva:<br>
Mensagem: Iniciar Contagem Regressiva<br>
Head: contagem_regressiva<br>

- Sua Vez:<br>
Mensagem: É a Sua Vez de Jogar<br>
Head: sua_vez<br>

- Turno do Adversário:<br>
Mensagem: É o Turno do Adversário<br>
Head: adversario<br>

- Jogada Realizada:<br>
Mensagem: Jogada Realizada pelo Adversário<br>
Head: jogada<br>

- Fim de Jogo:<br>
Mensagem: Fim de Jogo com Resultado<br>
Head: fim_de_jogo<br>

### 3 - Comandos do Cliente para o servidor:

- Conectar ao Servidor:<br>
Comando: Conectar ao Servidor<br>
Role: cliente<br>
Ação: conectar<br>

- Realizar Jogada:<br>
Comando: Realizar Jogada no Tabuleiro<br>
Role: jogador1 ou jogador2<br>
Ação: jogada<br>


<h1 align = 'center'>Estruturação e organização do projeto</h1>

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

<h2>- Confiabilidade na Entrega de Dados:</h2>
<p>O protocolo TCP garante a entrega confiável de dados entre o cliente e o servidor. Isso é crucial para garantir que todas as movimentações dos jogadores e a colocação de barreiras sejam recebidas e processadas corretamente, sem perda de informações durante a transmissão.</p>

<h2>- Ordem de Entrega:</h2>
<p>A ordem em que as mensagens são enviadas e recebidas é preservada pelo TCP. Em um jogo com turnos definidos, como é o caso aqui, manter a ordem correta das ações é vital para garantir a sincronização entre os jogadores, assegurando uma experiência de jogo coesa.</p>

<h2>- Controle de Congestionamento:</h2>
<p>O TCP incorpora mecanismos eficientes de controle de congestionamento, evitando sobrecargas na rede. Isso é crucial para garantir um desempenho estável do jogo, mesmo em condições de tráfego intenso na rede.</p>

<h2>- Segurança na Comunicação:</h2>
<p>O TCP fornece um nível adicional de segurança, garantindo que os dados transmitidos entre o cliente e o servidor não sejam comprometidos durante a transferência. Isso é crucial para impedir manipulações indesejadas que poderiam afetar a integridade do jogo.</p>

<p>Em resumo, a escolha do protocolo TCP para a comunicação entre o cliente e o servidor neste jogo  é fundamentada na busca por uma comunicação robusta, confiável e ordenada, elementos cruciais para garantir uma experiência de jogo fluida e sem contratempos para os jogadores envolvidos.</p>

<h1 align = 'center'>Funcionamento do Software</h1>
<p>O funcionamento do jogo será documentado em tópicos, sendo cada tópico uma classe da aplicação e logo depois uma explicação dela:</p>

### Servidor (server.py):
- Inicia um servidor TCP e aguarda conexões de dois jogadores.<br>
- Cria instâncias de Jogador para representar cada jogador, atribuindo a eles papéis ("jogador1" e "jogador2").<br>
- Inicia threads para tratar mensagens de cada jogador (tratar_mensagem).<br>
- Realiza uma contagem regressiva antes do início do jogo.<br>
- Inicia o jogo, informando ao jogador 1 que é sua vez (sua_vez) e ao jogador 2 que é o turno do adversário (adversario).<br>
- Troca mensagens entre jogadores conforme eles realizam movimentos ou colocam barreiras.<br>

### Cliente (client.py):
- Cria uma interface gráfica (Tabuleiro) usando a biblioteca Tkinter.<br>
- Conecta-se ao servidor através de um socket.<br>
- Recebe mensagens do servidor, atualiza a interface do usuário e permite a interação do jogador.<br>

### Tabuleiro (tabuleiro.py):
- Desenha o tabuleiro de jogo, jogadores, e barreiras utilizando a biblioteca Tkinter.<br>
- Conecta-se ao servidor para receber mensagens e enviar comandos.<br>
- Atualiza a interface do usuário com base nas mensagens recebidas.<br>
- Permite que o jogador 1 se mova com as teclas de seta e o jogador 2 coloque barreiras com cliques do mouse.<br>

### Jogadores (jogador1.py e jogador2.py):
- Implementam a lógica específica de movimento para o jogador 1 (Jogador1) e a lógica de colocação de barreiras para o jogador 2 (Jogador2).<br>
- Envia comandos para o servidor informando movimentos ou a colocação de barreiras.<br>
- Atualiza a interface do usuário no tabuleiro com base nas mensagens recebidas.<br>

## Fluxo de Mensagens: 
1. Jogador 1 se move usando teclas de seta.
2. Tabuleiro envia mensagem "jogada" para o servidor com as coordenadas do movimento.
3. Servidor repassa a mensagem para Jogador 2.
4. Jogador 2 coloca uma barreira usando o mouse.
5. Tabuleiro envia mensagem "jogada" para o servidor com as coordenadas da barreira.
6. Servidor repassa a mensagem para Jogador 1.
7. Repete até o fim do jogo.

<h1 align = 'center'>Propósito do Software</h1>
<p>É um projeto da matéria de redes do curso de Ciência da Computação que tem o propósito de fornecer uma experiência de jogo interativa e desafiadora para dois jogadores, envolvendo estratégia. O jogo busca proporcionar diversão enquanto promove a competição amigável entre os participantes.</p>

<h1 align = 'center'>Requisitos Mínimos</h1>
<p>Uma computador com sistema operacional Linux ou Windows</p>
<p>Python 3 instalado</p>
<p>Conexão de rede entre os jogadores</p>
<p>Capacidade de executar sockets TCP</p>

<h1 align = 'center'>Conclusão</h1>
<p>Este jogo oferece uma experiência dinâmica e estratégica, facilitada pela comunicação eficiente proporcionada pelo protocolo TCP. A documentação do protocolo e do software visa facilitar o entendimento e aprimoramento contínuo deste projeto. Divirta-se jogando!
</p>
