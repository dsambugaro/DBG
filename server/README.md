## Server

Pré-requisitos:
```
Python 3.x
Mongodb 4.4.x
```


Dependências python:
```
pymongo==3.11.0
paho-mqtt==1.5.1
PyYAML==5.3.1
```

Para instalar as dependências:

```bash
$ pip install -r requeriments.txt
```

Para executar o servidor:

```bash
$ python main.py
```

Arquivo de configuração:

```YAML
connection:
  host: mqtt.eclipse.org
  port: 1883
  QoS: 1
  username: null
  password: null
encoding: utf-8
```

* `connection` é a configuração de conexão do MQTT
  * `host` é o endereço do broker MQTT
  * `port` é a porta do broker MQTT
  * `QoS` é a qualidade de serviço utilizada para enviar mensagens MQTT
  * `username` é o usuário de autenticação MQTT se necessário
  * `password` é a senha de autenticação MQTT se necessário
* `encoding` é o tipo de codificação utilizado para codificar e decofidicar os bytes das mensagens MQTT
