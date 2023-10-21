# GorZdrav bot :sparkles:

Telegram bot that tracks appointments on GorZdrav and notifies the user

## Requirements :memo:
* Python >=3.11
* Postgresql
* Redis (optional)

## Configuration :wrench:
#### Global settings
* **log_level** - Log level (debug, info, error)
* **use_redis** - Use redis (True of False)
* **use_webhook** - Use webhook (True of False)
* **check_every** - Check interval in minutes (integer)

#### Telegram settings
* **bot__token** - Bot token (string)

#### DataBase settings
* **db__host** - Database host (string)
* **db__port** - Database port (integer)
* **db__user** - Database user (string)
* **db__password** - Database password (string)
* **db__database** - Database database (string)

#### Redis settings
* **redis__host** - Redis host (string)
* **redis__port** - Redis port (integer)
* **redis__password** - Redis password (string)

#### Webhook settings
* **webhook__url** - Webhook URL (string)
* **webhook__path** - Webhook path (string)
* **webhook__server_host** - Webhook server host (string)
* **webhook__server_port** - Webhook server port (integer)