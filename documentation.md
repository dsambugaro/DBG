# Documentation

## Table of contents
* [Arquitetura](#arquitetura)
    * [Tecnologias](#tecnologias)
    * [Ilustração](#ilustração)
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
- A implementação do cliente será realizada em **Python *OU* Javascript** -> definição ainda pendente
- A implementação do servidor será realizada em **Python**
- A persistencia dos dados será feita com **MongoDB**
- O Servidor ficará hospedado em uma das plataformas: **AWS**, **DigitalOcean** ou **Google Cloud Platform**

### Ilustração
![Arquitetura geral](/arquitetura.png)

-----------

## Interface

### Gerenciador de Jogadores:
- Criar novo jogador
- Buscar jogadores online
- Buscar jogador "x"
- Desafiar jogador

### Gerenciador de Partidas:
- Encontrar partida
- Iniciar partida
- Sair da partida
- Desistir da partida
- Contabilizar Ranking

### Gerenciador de Ranking:
- Atualizar Ranking
- Buscar Ranking
- Ordenar Ranking
- Filtrar Ranking
