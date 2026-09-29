import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline

app = FastAPI(title="EduGenie", description="Offline Local Learning Assistant")

# Setup safe base directory paths for templates and static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Load local Hugging Face model (No API key needed!)
print("Loading local AI model... Please wait a second...")
local_generator = pipeline('text2text-generation', model='MBZUAI/LaMini-Flan-T5-783M')

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/api/ask")
async def ask_local_ai(topic: str):
    try:
        prompt = f"Provide clear study notes and bullet points for the topic: {topic}"
        result = local_generator(prompt, max_length=256, do_sample=False)
        notes = result[0]['generated_text']
        return {"notes": notes}
    except Exception as e:
        return {"notes": f"Error: {str(e)}"}