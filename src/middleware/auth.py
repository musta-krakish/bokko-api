import hashlib
import hmac
import json
import time
from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from pydantic import BaseModel
from typing import Optional
from config import TELEGRAM_TOKEN

telegram_authentication_schema = HTTPBase(scheme="twa")


# Модель для Telegram User
class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    is_premium: Optional[bool]
    allows_write_to_pm: Optional[bool]


# Функция для валидации initData
def validate_telegram_auth(init_data: dict, auth_date_threshold: int = 86400) -> TelegramUser:
    # 86400 секунд = 24 часа
    auth_date = init_data.get("auth_date")
    
    if not auth_date or int(time.time()) - int(auth_date) > auth_date_threshold:
        raise HTTPException(status_code=403, detail="Authentication expired.")

    # Создание строки для хеширования
    data_check_string = "\n".join(
        [f"{k}={init_data[k]}" for k in sorted(init_data) if k != "hash"]
    )
    
    # Генерация хэша с использованием SHA-256 и секретного ключа
    secret_key = hashlib.sha256(TELEGRAM_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Проверка хэша
    if calculated_hash != init_data.get("hash"):
        raise HTTPException(status_code=403, detail="Invalid hash.")

    # Вернуть объект пользователя, если всё прошло успешно
    return TelegramUser(**init_data["user"])


# Middleware для получения текущего пользователя
def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
) -> TelegramUser:
    if not auth_cred or not auth_cred.credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization credentials."
        )

    # Декодируем строку initData
    try:
        init_data = json.loads(auth_cred.credentials)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid init data format.")

    # Валидация initData
    try:
        user = validate_telegram_auth(init_data)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    return user
