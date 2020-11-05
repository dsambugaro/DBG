## Server

Pré-requisitos:
```
Python 3.x
```


Dependências python:
```
emoji==0.6.0
paho-mqtt==1.5.1
PyYAML==5.3.1
```

Para instalar as dependências:

```bash
$ pip install -r requeriments.txt
```

Para executar o cliente:

```bash
$ python main.py
```

Arquivo de configuração:

```YAML
UUID: null
connection:
  QoS: 1
  host: mqtt.eclipse.org
  port: 1883
  username: null
  password: null
encoding: utf-8
pretty: true

```

* `UUID` é um identificador único do cliente, gerado automaticamente na primeira vez em que a aplicação é executada
* `connection` é a configuração de conexão do MQTT
  * `host` é o endereço do broker MQTT
  * `port` é a porta do broker MQTT
  * `QoS` é a qualidade de serviço utilizada para enviar mensagens MQTT
  * `username` é o usuário de autenticação MQTT se necessário
  * `password` é a senha de autenticação MQTT se necessário
* `encoding` é o tipo de codificação utilizado para codificar e decofidicar os bytes das mensagens MQTT
* `pretty` é a configuração que diz se os emojis estaram habilitados ou desabilitados
