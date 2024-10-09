from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from middleware.auth import TelegramUser
from models.goal_models import TaskModel
from utils.serialize import get_serialize_document
from datetime import datetime
import bson

router = APIRouter()

@router.post("/")
async def create_task(goal_id: str,
                      request: TaskModel,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    goal_document = await repo.find_one("goals", 
                                        {"_id": bson.ObjectId(goal_id), "tg_id": user.id})
    if not goal_document:
        raise HTTPException(404, "goal not found")
    document = request.model_dump()
    document["goal_id"] = goal_id
    document["create_date"] = datetime.now()
    document["tg_id"] = user.id
    await repo.insert_one("tasks", document)
    return {"detail": "document successfully create"}

@router.get("/")
async def fetch_tasks(goal_id: str | None = None,
                      date: datetime | None = None,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    if goal_id:
        goal_document = await repo.find_one("goals", {"_id": bson.ObjectId(goal_id), "tg_id": user.id})
        if not goal_document:
            raise HTTPException(404, "goal not found")
    
    if date:
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        query = {
            "deadline": {"$gte": start_of_day, "$lte": end_of_day},
            "tg_id": user.id
        }
        if goal_id:
            query["goal_id"] = goal_id
        
        tasks = await repo.find_many("tasks", query)
    
    else:
        query = {}
        if goal_id:
            query["goal_id"] = goal_id  
        else:
            query["tg_id"] = user.id  
        
        tasks = await repo.find_many("tasks", query)
    
    return await get_serialize_document(tasks)

@router.put("/confurm/")
async def confurm_task(task_id: str,
                       repo: Repository = Depends(get_repository),
                       user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("tasks", {"_id": bson.ObjectId(task_id), "tg_id": user.id})
    if not document:
        raise HTTPException(404, "task not found")
    await repo.update_one("tasks", {"_id": bson.ObjectId(task_id)}, {"complite": True, "end_date": datetime.now()})
    return {"detail": "document successfully update"}

@router.delete("/")
async def delete_task(task_id: str,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("tasks", {"_id": bson.ObjectId(task_id), "tg_id": user.id})
    if not document:
        raise HTTPException(404, "task not found")
    await repo.delete_one("tasks", {"_id": bson.ObjectId(task_id), "tg_id": user.id})
    return {"detail": "document successfully delete"}