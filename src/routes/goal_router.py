from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from middleware.auth import TelegramUser
from models.goal_models import GoalModel
from utils.serialize import get_serialize_document
import bson

router = APIRouter()

@router.post("/")
async def create_goal(request: GoalModel,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    document["tg_id"] = user.id
    ins_id = await repo.insert_one("goals", document)
    return {"detail":"document succesfully create", "_id": str(ins_id)}

@router.get("/")
async def fetch_goals(repo: Repository = Depends(get_repository),
                    user: TelegramUser = Depends(get_current_user)):
    documents = await repo.find_many("goals", {"tg_id": user.id})
    return await get_serialize_document(documents)

@router.delete("/")
async def delete_goal(id: str,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("goals", {"tg_id": user.id, "_id": bson.ObjectId(id)})
    if not document:
        raise HTTPException(404, "document not found")
    await repo.delete_one("goals", {"tg_id": user.id, "_id": bson.ObjectId(id)})
    return {"detail":"document succesfully delete"}