import uvicorn
import asyncio
from demon.schreduler import run_schreduler

async def start_scheduler():
    await run_schreduler()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scheduler_task = loop.create_task(start_scheduler())  
    uvicorn_task = loop.create_task(uvicorn.run("app:app", host="127.0.0.1", port=8000))  

    loop.run_until_complete(asyncio.gather(scheduler_task, uvicorn_task))