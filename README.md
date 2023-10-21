# GorZdrav bot :sparkles:

Telegram bot that tracks appointments on GorZdrav and notifies the user

## Requirements :memo:
* Python >=3.11
* Postgresql
* Redis (optional)

## Configuration :wrench:
### Global settings
* log_level = "(str) Log level (debug, info, error)"
* use_redis = "(bool) Use redis"
* use_webhook: "(bool) Use webhook"
* check_every = "(int) Check appointments every minutes"

### Tg bot settings
* bot__token="(str) Bot token"

### DataBase settings
* db__host="(str) Database host"
* db__port="(int) Database port"
* db__user="(str) Database user"
* db__password="(str) Database password"
* db__database="(str) Database name"

### Redis settings
* redis__host="(str) Redis host"
* redis__port="(int) Redis port"
* redis__password="(str) Redis password"

### Webhook settings
* webhook__url = "(str) Webhook URL"
* webhook__path = "(str) Webhook path"
* webhook__server_host = "(str) Webhook server host"
* webhook__server_port = "(int) Webhook server port"