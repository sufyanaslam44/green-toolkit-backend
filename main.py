from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="Green Toolkit")

# Serve /static if you later add custom JS/CSS/images
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Data we can inject into the template
    context = {
        "request": request,
        "title": "Green Toolkit",
        "subtitle": "We are ready to build green tool",
    }
    return templates.TemplateResponse("index.html", context)
