# GorZdrav bot :sparkles:

Telegram bot that tracks appointments on GorZdrav and notifies the user

## Requirements :memo:
* Python >=3.11
* Postgresql
* Redis (optional)

## Configuration :wrench:
The settings should be in the .env file or in the environment variables

#### Global settings
* **GORZDRAV_LOG_LEVEL** - (str) Log level (debug, info, error) (default: INFO)
* **GORZDRAV_USER_REDIS** - (bool) Use redis (default: False)
* **GORZDRAV_USE_WEBHOOK** - (bool) Use webhook (default: False)
* **GORZDRAV_CHECK_EVERY** - (int) Check appointments every (VALUE) minutes (default: 5)

#### Telegram settings
* **GORZDRAV_BOT__TOKEN** - (str) Bot token

#### DataBase settings
* **GORZDRAV_DB__HOST** - (str) Database host (default: localhost)
* **GORZDRAV_DB__PORT** - (int) Database port (default: 5432)
* **GORZDRAV_DB__USER** - (str) Database user
* **GORZDRAV_DB__PASSWORD** - (str) Database password
* **GORZDRAV_DB__DATABASE** - (str) Database name

#### Redis settings
* **GORZDRAV_REDIS__HOST** - (str) Redis host (default: localhost)
* **GORZDRAV_REDIS__PORT** - (int) Redis port (default: 6379)
* **GORZDRAV_REDIS__PASSWORD** - (str) Redis password (default: None)

#### Webhook settings
* **GORZDRAV_WEBHOOK__DOMAIN** - (str) Webhook domain (example.com[:PORT])
* **GORZDRAV_WEBHOOK__PATH** - (str) Webhook path (default: /webhook)
* **GORZDRAV_WEBHOOK__APP_HOST** - (str) Webhook app interface (default: 0.0.0.0)
* **GORZDRAV_WEBHOOK__APP_PORT** - (int) Webhook app port (default: 80)

## How to run :hammer_and_wrench:
```
git clone https://github.com/Kllraz/gorzdrav_bot
cd gorzdrav_bot
```

Create .env file and fill it with the settings

Run `docker compose up -d`

If you`re using Traefik as the reverse proxy, check the network and the certificate resolver in compose.taefik.yaml

Run `docker compose -f compose.yaml -f compose.traefik.yaml up -d`