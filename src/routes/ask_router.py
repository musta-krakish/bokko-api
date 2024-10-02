from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from telegram_webapp_auth.auth import TelegramUser
from utils.promt import ask_decomposing
import bson

router = APIRouter()

@router.post("/decomposing/")
async def fetch_motivate(goal_id: str,
                         repo: Repository = Depends(get_repository),
                         user: TelegramUser = Depends(get_current_user)):
    docoment = await repo.find_one("goals", {"_id": bson.ObjectId(goal_id), "tg_id": user.id})
    if not docoment:
        raise HTTPException(404, "document not found")
    response = await ask_decomposing(docoment["title"], docoment["description"])
    return {"detail": response}


@router.post("/motivation/")
async def fetch_motivation():
    return True

