from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import app_logic
import database
import schedule
import threading
import multipart

database.vytvor_tabulky()
app_logic.get_rates()
schedule.every().day.at("15:00").do(app_logic.job)
scheduler_thread = threading.Thread(target=app_logic.run_scheduler)
scheduler_thread.start()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.route("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/prijmy")
async def prijmy(request: Request):
    return templates.TemplateResponse("prijmy.html", {"request": request})

@app.post("/prijmy", response_class=HTMLResponse)
async def zadej_prijem(request: Request):
    form_data = await request.form()
    prijem = form_data.get("prijem_input")
    mena = form_data.get("mena")
    datum = form_data.get("datum_input")
    cas = form_data.get("cas_input")
    popis = form_data.get("prijem_popis")
    database.pridej_prijem_do_db(prijem, mena, datum, cas, popis)
    return RedirectResponse(url="/prijmy", status_code=303)

@app.get("/registrace")
async def registrace(request: Request):
    return templates.TemplateResponse("registrace.html", {"request": request})

@app.post("/registrace", response_class=HTMLResponse)
async def zadej_registraci(request: Request):
    form_data = await request.form()
    mail = form_data.get("mail")
    uzivatel = form_data.get("uzivatel_input")
    heslo = form_data.get("heslo")
    heslo_znovu = form_data.get("heslo_znovu")
    if uzivatel != database.uzivatel_check(uzivatel) and mail != database.mail_check(mail) and heslo == heslo_znovu:
        database.pridej_uzivatele_do_db(mail, uzivatel, heslo)
        return RedirectResponse(url="/prihlaseni", status_code=303)
    else:
        return RedirectResponse(url="/registrace", status_code=303)
    
@app.get("/prihlaseni")
async def prihlaseni(request: Request):
    return templates.TemplateResponse("prihlaseni.html", {"request": request})

@app.post("/prihlaseni", response_class=HTMLResponse)
async def zadej_prihlaseni(request: Request):
    form_data = await request.form()
    uzivatel = form_data.get("uzivatel_input")
    heslo = form_data.get("heslo")
    if uzivatel == database.uzivatel_check(uzivatel) and heslo == database.heslo_check(uzivatel):
            return RedirectResponse(url="/souhrn", status_code=303)
    else:        
        return RedirectResponse(url="/prihlaseni", status_code=303)


@app.get("/vydaje")
async def vydaje(request: Request):
    return templates.TemplateResponse("vydaje.html", {"request": request})

@app.post("/vydaje", response_class=HTMLResponse)
async def zadej_vydaje(request: Request):
    form_data = await request.form()
    vydaj = form_data.get("vydaj_input")
    mena = form_data.get("mena")
    datum = form_data.get("datum_input")
    cas = form_data.get("cas_input")
    popis = form_data.get("vydaj_popis")
    database.pridej_vydaj_do_db(vydaj, mena, datum, cas, popis)
    return RedirectResponse(url="/vydaje", status_code=303)

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