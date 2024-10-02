from config import DATABASE_NAME, DATABASE_URL
from data.repository import Repository
import asyncio
from time import sleep
from datetime import datetime
from utils.telegram import send_message

async def get_schredule_task(repo: Repository):
    current_date = datetime.now()
    start_of_day = datetime(current_date.year, current_date.month, current_date.day)
    end_of_day = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)
    tasks = await repo.find_many("tasks", {"deadline": {"$gte": start_of_day, "$lte": end_of_day}})
    return tasks

async def run_schreduler():
    repo = Repository(DATABASE_URL, DATABASE_NAME)
    while True:
        tasks = get_schredule_task(repo)
        for task in tasks:
            await send_message(task["tg_id"],
                               f"Привет дружище, дедлайн задачи {task["title"]} сгорает сегодня. Может пора взяться?"
                               )
            sleep(1)
            await asyncio.sleep(8 * 60 * 60)