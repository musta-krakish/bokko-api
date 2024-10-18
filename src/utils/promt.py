from data.gemini import Gemini
from config import GEMINI_API_KEY

gemini = Gemini(
    key=GEMINI_API_KEY
)

async def ask_decomposing(title: str, text: str) -> str:
    promt_text = f"Привет, ты самый лучший персональный тьютор, можешь декомпозировать цель: {title} и расписать возможные ее задачи вот ее описание {text}. отвечай эмоционально и можешь использовать эмодзи"
    result = await gemini.ask(promt_text)
    return result

async def ask_motivation(title: str, tasks: list ):
    return