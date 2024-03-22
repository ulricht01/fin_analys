import requests
from bs4 import BeautifulSoup
import database
import time
import schedule
import uuid


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
                
    database.pridej_kurz_do_db("EUR", eur)
    database.pridej_kurz_do_db("USD", usd)

    
def job():
    get_rates()    
    
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)       
        
def generate_session_id(current_user_id):
    database.pridej_session(str(uuid.uuid4()), current_user_id)

def verify_session(session_id):
    if database.select_session(session_id) == None:
        return False
    else:
        return True   
    