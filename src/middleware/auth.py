from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase

from telegram_webapp_auth.auth import TelegramAuthenticator
from telegram_webapp_auth.auth import TelegramUser
from telegram_webapp_auth.auth import generate_secret_key
from telegram_webapp_auth.errors import InvalidInitDataError

from config import TELEGRAM_TOKEN

telegram_authentication_schema = HTTPBase(scheme="twa")

def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(TELEGRAM_TOKEN)
    return TelegramAuthenticator(secret_key)

def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
) -> TelegramUser:
    try:
        user = telegram_authenticator.verify_token(auth_cred.credentials)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=403,
            detail="Forbidden access.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal error.",
        )

    return user