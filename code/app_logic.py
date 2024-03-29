import requests
from bs4 import BeautifulSoup
import database
import time
import schedule
import uuid
import re
import datetime


def get_rates():
    url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="currency-table")
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        for column in columns:
            if "USD" in column.text:
                usd = float(columns[4].text.replace(",", "."))
            elif "EUR" in column.text:
                eur = float(columns[4].text.replace(",", "."))
            elif "GBP" in column.text:
                gbp = float(columns[4].text.replace(",", "."))
                
    database.pridej_kurz_do_db("EUR", eur)
    database.pridej_kurz_do_db("USD", usd)
    database.pridej_kurz_do_db("GBP", gbp)

    
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(5)      
        
def end_inactive_sessions():
    # Získání aktuálního času
    current_time = datetime.datetime.now()

    # Získání všech session z databáze
    all_sessions = database.get_all_sessions()

    # Kontrola zda je seznam sessions prázdný
    if not all_sessions:
        return  None

    # Pro každou session
    for session in all_sessions:
        # Vypočítat čas od poslední aktivity
        time_since_last_activity = current_time - session['posledni_aktivita']

        # Pokud čas od poslední aktivity je větší než 30 minut
        if time_since_last_activity.total_seconds() > 1800:  # 1800 sekund = 30 minut
            # Ukončit session
            end_session(session['id'])

# Funkce pro ukončení session
def end_session(session_id):
    database.odeber_session(session_id) 
        
def generate_session_id(current_user_id):
    database.pridej_session(str(uuid.uuid4()), current_user_id)

def verify_session(session_id):
    if database.select_session(session_id) == None:
        return False
    else:
        return True   
    
def check_password_reg(heslo, uzivatel, mail, heslo_znovu):
    if len(heslo) < 8:
        return False, "Heslo je přílíš krátké!"
    
    if not re.search("[A-Z]", heslo):
        return False, "Heslo musí obsahovat alespoň jedno velké písmeno!"
    
    if not re.search("[0-9]", heslo):
        return False, "Heslo musí obsahovat alepsoň jedno číslo!"
    
    if not database.uzivatel_check(uzivatel) == None:
        return False, "Uživatel již existuje!"
    
    if not database.mail_check(mail) == None:
        return False, "Email již existuje!"
    
    if not heslo == heslo_znovu:
        return False, "Hesla se neshodují!"
    
    return True, "Úspěšná registrace!"

def get_bitcoin_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=czk'
        response = requests.get(url)
        data = response.json()
        bitcoin_price_czk = data['bitcoin']['czk']
        database.pridej_krypto_do_db("BITC", bitcoin_price_czk)
    except KeyError as e:
        print("Chyba při získávání ceny Bitcoinu:", e)
    except Exception as e:
        print("Neočekávaná chyba při získávání ceny Bitcoinu:", e)

def get_shiba_inu_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=shiba-inu&vs_currencies=czk'
        response = requests.get(url)
        data = response.json()
        shiba_inu_price_czk = data.get('shiba-inu', {}).get('czk')
        if shiba_inu_price_czk is not None:
            database.pridej_krypto_do_db("SHIB", shiba_inu_price_czk)
    except Exception as e:
        print("Neočekávaná chyba při získávání ceny Shiba Inu:", e)

def get_dogecoin_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=czk'
        response = requests.get(url)
        data = response.json()
        dogecoin_price_czk = data.get('dogecoin', {}).get('czk')
        if dogecoin_price_czk is not None:
            database.pridej_krypto_do_db("DOGE", dogecoin_price_czk)
    except Exception as e:
        print("Neočekávaná chyba při získávání ceny Dogecoinu:", e)
