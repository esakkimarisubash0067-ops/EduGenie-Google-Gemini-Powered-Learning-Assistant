import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class TopicRequest(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Combined endpoint to handle JSON or Form data
@app.post("/generate")
@app.post("/explain")
async def generate_notes(request: Request):
    try:
        data = await request.json()
        topic = data.get("topic", "Python Functions")
    except Exception:
        form_data = await request.form()
        topic = form_data.get("topic", "Python Functions")

    response_text = f"Study Notes for '{topic}':\n\n1. Definition: A function is a block of organized, reusable code used to perform a single, related action.\n2. Syntax: Defined using the 'def' keyword.\n3. Benefits: Code reusability, modularity, and better readability."

    # Return key names covering all possible frontend JS property checks
    return JSONResponse(content={
        "notes": response_text,
        "explanation": response_text,
        "result": response_text,
        "text": response_text
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

