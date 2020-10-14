# Documentation

## Table of contents
* [Arquitetura](#arquitetura)
    * [Tecnologias](#tecnologias)
    * [Diagramas e fluxo](#diagramas-e-fluxo)
* [Interface](#interface)
    * [Gerenciador de Jogadores](#gerenciador-de-jogadores)
    * [Gerenciador de Partidas](#gerenciador-de-partidas)
    * [Gerenciador de Ranking](#gerenciador-de-ranking)


## Arquitetura

A arquitetura será *baseada em eventos*, no modelo Publish / Subscriber.
O cliente irá consumir e gerar eventos conforme a ação sendo executada pelo usuário.
O servidor será constituído por *microsserviços* que irão consumir e gerar eventos e dados:
- Gerenciador de partidas: Responsável por criar e gerenciar partidas
- Gerenciador de jogadores: Responsável por cadastrar novos jogadores e gerenciar a interação entre eles
- Gerenciador de Ranking: Responsável por registrar, ordenar e filtrar os pontos dos jogadores 

### Tecnologias
- Para o gerenciamento dos eventos no modelo Publish / Subscriber será realizado pelo **Apache Kafka**
- A implementação do cliente será realizada em **Python**
- A implementação do servidor será realizada em **Python**
- A persistencia dos dados será feita com **MongoDB**
- O Servidor ficará hospedado em uma das plataformas: **AWS**, **DigitalOcean** ou **Google Cloud Platform**

### Diagramas e fluxo
Diagrama geral da arquitetura:
![Arquitetura geral](/arquitetura.png)

O fluxo de um jogo é dividido em algumas etapas:

* **Etapa 1**: Os jogadores entram na fila para encontrar uma partida, o gerenciador de partidas combina os jogadores e inicia uma nova partida.

    Cada jogador gera um evento de encontrar partida que será consumido pelo gerenciador de partidas. Uma nova partida gera um evento de partida encontrada indicando aos jogadores participantes que podem posicionar seuas embarcações.

Diagrama da etapa 1:
![Etapa 1 do fluxo do jogo](/1.png)

* **Etapa 2**: Os jogadores posicionam suas embarcações, quando ambos tiveram finalizado essa terefa a partida se inicia.

    Cada jogador ao finalizar de posicionar suas embarcações gera um evento de embarcações posicionadas, o processo de partida aguarda receber o evento de ambos os jogadores, escolhe aleatóriamente um jogador para jogar primeiro e gera um evento de partida iniciada que indica aos jogadores o inicio do jogo.

Diagrama da etapa 2:
![Etapa 2 do fluxo do jogo](/2.png)

* **Etapa 3**: Os jogadores realizam suas jogadas alternadamente, as jogadas são processadas pelo servidor e o resultado delas são enviadas para os jogadores.

    Ao realizar uma jogada o jogador gera um evento de jogada realizada. A partida processa a jogada e retorna o resultado dela para ambos os jogadores. Esse processo se repete, com cada joghador realziando a jogada de forma alternada, até o fim da partida.

Diagrama da etapa 3:
![Etapa 3 do fluxo do jogo](/3.png)

Após uma jogada levar ao evento de fim de partida, os jogadores recebem esse evento informando o jogador vencedor. O mesmo evento também será publicado no tópico do gerenciador de ranking para que ele possa atualizar devidamente a pontuação do jogador vencedor.

-----------

## Interface

### Gerenciador de Jogadores:
- Criar novo jogador
    - Retorna o UUID do jogador em caso de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Buscar jogadores online
    - Retorna uma lista com os jogadores online
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Buscar jogador "x"
    - Retorna uma mensagem com os dados do jogador em casos de sucesso
    - Retorna uma mensagem de jogador não encontrado se o jogador não existir
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Desafiar jogador
    - Retorna uma confirmação de desafio enviado em caso de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha

### Gerenciador de Partidas:
- Encontrar partida
    - Retorna a confirmação de entrada na fila em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Iniciar partida
    - Retorna os dados da nova partida em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Desistir da partida
    - Retorna a conformação da rendição em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Contabilizar Ranking
    - Retorna a nova posição no ranking em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha

### Gerenciador de Ranking:
- Atualizar Ranking
    - Retorna a lista de ranking atualizada em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Buscar Ranking do jogador "x"
    - Retorna o ranking do jogador em casos de sucesso
    - Retorna uma mensagem de ranking não encontrado caso não exista ranking para aquele jogador
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Ordenar Ranking
    - Retorna o ranking ordenado pela característica pedida em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
- Filtrar Ranking
    - Retorna o ranking com os filtros escolhidos aplicados em casos de sucesso
    - Retorna uma mensagem com a descrição do erro em casos de falha
