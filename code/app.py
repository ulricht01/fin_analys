from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import app_logic

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.route("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.route("/prijmy")
async def main_page(request: Request):
    return templates.TemplateResponse("prijmy.html", {"request": request})

@app.route("/vydaje")
async def main_page(request: Request):
    return templates.TemplateResponse("vydaje.html", {"request": request})

@app.route("/kurzy")
async def main_page(request: Request):
    rate_usd = app_logic.get_rate_usd()
    rate_eur = app_logic.get_rate_eur()
    return templates.TemplateResponse("kurzy.html", {"request": request, "usd_rate": rate_usd, "eur_rate": rate_eur})

@app.route("/souhrn")
async def main_page(request: Request):
    return templates.TemplateResponse("souhrn.html", {"request": request})