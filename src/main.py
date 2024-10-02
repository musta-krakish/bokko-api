import uvicorn
import asyncio
from demon.schreduler import run_schreduler

if __name__ == "__main__":
    asyncio.run(run_schreduler())
    uvicorn.run("app:app", host="127.0.0.1", port=8000)