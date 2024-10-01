from fastapi import APIRouter, Depends
from data.repository import Repository
from data.depends import get_repository
from telegram_webapp_auth.auth import TelegramUser
from middleware.auth import get_current_user
from models.user_models import UserModel
from utils.serialize import get_serialize_document

router = APIRouter()

@router.post("/register/")
async def register_user(request: UserModel, 
                        repo: Repository = Depends(get_repository),
                        user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    document["tg_id"] = user.id
    await repo.insert_one("users", document)
    return {"detail":"document successfull create"}

@router.put("/")
async def change_user(request: UserModel,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    await repo.update_one("users", {"tg_id": user.id}, document)
    return {"detail":"document successfull update"}

@router.get("/me/")
async def fetch_me(repo: Repository = Depends(get_repository),
                   user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("users", {"tg_id": user.id})
    return await get_serialize_document(document)

