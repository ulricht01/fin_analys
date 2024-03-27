from fastapi import FastAPI, Request, Depends, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import app_logic
import database
import schedule
import threading
import hashlib


database.vytvor_tabulky()
app_logic.get_rates()
schedule.every().day.at("15:00").do(app_logic.job)
schedule.every(5).minutes.do(app_logic.run_scheduler)
scheduler_thread = threading.Thread(target=app_logic.run_scheduler)
scheduler_thread.start()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/obrazky", StaticFiles(directory="templates/obrazky"), name="obrazky")

@app.get("/")
async def main_page(request: Request, session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):  # Check for valid session
        return RedirectResponse(url="/souhrn", status_code=303)
    else:
        return RedirectResponse(url="/prihlaseni", status_code=303)
    
@app.get("/prijmy")
async def prijmy(request: Request, success_mess: str ="", session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):  # Check for valid session
        kategorie= database.kategorie_prijmy()
        return templates.TemplateResponse("prijmy.html", {"request": request, "session_id": session_id, "success_mess": success_mess, "kategorie" : kategorie})
    else:
        return RedirectResponse(url="/prihlaseni", status_code=303)
   
@app.post("/prijmy", response_class=HTMLResponse)
async def zadej_prijem(request: Request, session_id: str = Cookie(None)):
    form_data = await request.form()
    prijem = form_data.get("prijem_input")
    mena = form_data.get("mena")
    datum = form_data.get("datum_input")
    cas = form_data.get("cas_input")
    kategorie = form_data.get("kategorie")
    id_uzivatele = database.get_user_id_via_session(request.cookies.get('session_id'))
    database.pridej_prijem_do_db(prijem, mena, datum, cas, kategorie, id_uzivatele)
    success_mess = "Úspěšně přidáno do příjmů!"
    return RedirectResponse(url=f"/prijmy?success_mess={success_mess}", status_code=303)

@app.get("/registrace")
async def registrace(request: Request, error_mess: str = "", session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):  # Check for valid session
        return RedirectResponse(url="/souhrn", status_code=303)
    else:
        return templates.TemplateResponse("registrace.html", {"request": request, "session_id": session_id, "error_mess": error_mess})


@app.post("/registrace", response_class=HTMLResponse)
async def zadej_registraci(request: Request, session_id: str = Cookie(None)):
    form_data = await request.form()
    mail = form_data.get("mail")
    uzivatel = form_data.get("uzivatel_input")
    heslo = form_data.get("heslo")
    heslo_znovu = form_data.get("heslo_znovu")
    heslo_encoded = heslo.encode('utf-8')
    heslo_hashed = hashlib.sha256(heslo_encoded).hexdigest()
    heslo_check_reg, mess = app_logic.check_password_reg(heslo, uzivatel, mail, heslo_znovu)
    if uzivatel != database.uzivatel_check(uzivatel) and mail != database.mail_check(mail) and heslo_check_reg == True:
        database.pridej_uzivatele_do_db(mail, uzivatel, heslo_hashed)
        sucess_mess = mess
        return RedirectResponse(url=f"/prihlaseni?success_mess={sucess_mess}", status_code=303)
    else:
        error_mess = mess
        return RedirectResponse(url=f"/registrace?error_mess={error_mess}", status_code=303)

@app.get("/prihlaseni")
async def prihlaseni(request: Request, error_mess: str = "", success_mess: str = "", session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):  # Check for valid session
        return RedirectResponse(url="/souhrn", status_code=303)
    else:
        return templates.TemplateResponse("prihlaseni.html", {"request": request, "session_id": session_id, "error_mess": error_mess, "success_mess": success_mess})

@app.post("/prihlaseni", response_class=HTMLResponse)
async def zadej_prihlaseni(request: Request, session_id: str = Cookie(None)):
    form_data = await request.form()
    uzivatel = form_data.get("uzivatel_input")
    heslo = form_data.get("heslo")
    heslo_encoded = heslo.encode('utf-8')
    heslo_hashed = hashlib.sha256(heslo_encoded).hexdigest()
    if uzivatel == database.uzivatel_check(uzivatel) and heslo_hashed == database.heslo_check(uzivatel):
        app_logic.generate_session_id(database.get_user_id(uzivatel))
        session_id = database.get_session_id(database.get_user_id(uzivatel))
        response = RedirectResponse(url="/souhrn", status_code=303)
        response.set_cookie(key="session_id", value=session_id)
        return response
    else: 
        error_mess = "Nesprávné přihlašovací údaje!"       
        return RedirectResponse(url=f"/prihlaseni?error_mess={error_mess}", status_code=303)

@app.get("/vydaje")
async def vydaje(request: Request, success_mess: str ="",session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):
        kategorie = database.kategorie_vydaje()
        return templates.TemplateResponse("vydaje.html", {"request": request, "session_id": session_id, "success_mess": success_mess, "kategorie": kategorie})
    else:
        return RedirectResponse(url="/prihlaseni", status_code=303)
    
@app.post("/vydaje", response_class=HTMLResponse)
async def zadej_vydaje(request: Request, session_id: str = Cookie(None)):
    form_data = await request.form()
    vydaj = form_data.get("vydaj_input")
    mena = form_data.get("mena")
    datum = form_data.get("datum_input")
    cas = form_data.get("cas_input")
    kategorie = form_data.get("kategorie")
    id_uzivatele = database.get_user_id_via_session(request.cookies.get('session_id'))
    database.pridej_vydaj_do_db(vydaj, mena, datum, cas, kategorie, id_uzivatele)
    success_mess = "Úspěšně přidáno do výdajů!"
    return RedirectResponse(url=f"/vydaje?success_mess={success_mess}", status_code=303)

@app.get("/kurzy")
async def kurzy(request: Request, session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):
        try:
            rate_usd = database.get_usd()
        except Exception as e:
            rate_usd = None
        try:
            rate_eur = database.get_eur()
        except Exception as e:
            rate_eur = None
        try:
            rate_gbp = database.get_gbp()
        except Exception as e:
            rate_gbp  = None
        return templates.TemplateResponse("kurzy.html", {"request": request, "usd_rate": rate_usd, "eur_rate": rate_eur, "gbp_rate": rate_gbp, "session_id": session_id})
    else:
        return RedirectResponse(url="/prihlaseni", status_code=303)

@app.get("/souhrn")
async def souhrn(request: Request, session_id: str = Cookie(None)):
    if session_id and app_logic.verify_session(session_id):
        return templates.TemplateResponse("souhrn.html", {"request": request, "session_id": session_id})
    else:
        return RedirectResponse(url="/prihlaseni", status_code=303)

@app.route("/odhlaseni")
async def odhlasit(request: Request, session_id: str = Cookie(None, description="Session ID", alias="session_id")):
    database.odeber_session(request.cookies.get('session_id'))
    response = RedirectResponse(url="/prihlaseni", status_code=303)
    response.delete_cookie("session_id")
    return response

@app.get("/prijmy_pie")
async def nacti_prijmy_pie(session_id: str = Cookie(None)):
    data= database.prijmy_pie_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/prijmy_bar")
async def nacti_bar_prijmy(session_id: str = Cookie(None)):
    data = database.prijmy_bar_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/prijmy_month_bar")
async def nacti_month_bar_prijmy(session_id: str = Cookie(None)):
    data = database.prijmy_month_bar_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/vydaje_pie")
async def nacti_prijmy_pie(session_id: str = Cookie(None)):
    data= database.vydaje_pie_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/vydaje_bar")
async def nacti_bar_prijmy(session_id: str = Cookie(None)):
    data = database.vydaje_bar_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/vydaje_month_bar")
async def nacti_month_bar_prijmy(session_id: str = Cookie(None)):
    data = database.vydaje_month_bar_data(database.get_user_id_via_session(session_id))
    return data

@app.get("/data_line_eur")
async def nacti_czk():
    data = database.nacti_eur_kurzy_line()
    return data

@app.get("/data_line_usd")
async def nacti_czk():
    data = database.nacti_usd_kurzy_line()
    return data

@app.get("/data_line_gbp")
async def nacti_czk():
    data = database.nacti_gbp_kurzy_line()
    return data