import json

with open('secrets.json') as arquivo_json:
    config = json.load(arquivo_json)

JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")
JWT_BLACKLIST_ENABLED = config.get("JWT_BLACKLIST_ENABLED")
MAILGUN_DOMAIN = config.get("MAILGUN_DOMAIN")
MAILGUN_API_KEY = config.get("MAILGUN_API_KEY")
SWAGGER_URL = config.get("SWAGGER_URL")
API_URL = config.get("API_URL")