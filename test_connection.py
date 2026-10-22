"""Smoke-тест: окружение, ключ, сертификат и доступность GigaChat API."""

import os

from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

credentials = os.getenv("GIGACHAT_CREDENTIALS")
ca_bundle = os.getenv("GIGACHAT_CA_BUNDLE_FILE")

print(f"Ключ авторизации: {credentials[:10]}..." if credentials else "КЛЮЧ НЕ НАЙДЕН")
print(f"CA-бандл: {ca_bundle}")

with GigaChat(
    credentials=credentials,
    scope="GIGACHAT_API_PERS",
    ca_bundle_file=ca_bundle,
    timeout=60.0,
) as client:
    token = client.get_token()
    print(f"Токен доступа получён, действует до: {token.expires_at}")

    models = client.get_models()
    print("Доступные модели:")
    for m in models.data:
        print(f"  {m.id_} (owned_by={m.owned_by})")