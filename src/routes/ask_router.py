from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from telegram_webapp_auth.auth import TelegramUser
from utils.serialize import get_serialize_document
import bson

router = APIRouter()

@router.post("/decomposing/")
async def fetch_motivate():
    return True    


@router.post("/motivation/")
async def fetch_motivation():
    return True

