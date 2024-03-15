from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import app_logic
import database
import schedule
import threading

database.vytvor_tabulky()
app_logic.get_rates()
schedule.every().hour.do(app_logic.job)
scheduler_thread = threading.Thread(target=app_logic.run_scheduler)
scheduler_thread.start()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.route("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.route("/prijmy")
async def prijmy(request: Request):
    return templates.TemplateResponse("prijmy.html", {"request": request})

@app.route("/vydaje")
async def vydaje(request: Request):
    return templates.TemplateResponse("vydaje.html", {"request": request})

@app.route("/kurzy")
async def kurzy(request: Request):
    try:
        rate_usd = database.get_usd()
    except Exception as e:
        rate_usd = None
    try:
        rate_eur = database.get_eur()
    except Exception as e:
        rate_eur = None
    return templates.TemplateResponse("kurzy.html", {"request": request, "usd_rate": rate_usd, "eur_rate": rate_eur})

@app.route("/souhrn")
async def souhrn(request: Request):
    return templates.TemplateResponse("souhrn.html", {"request": request})