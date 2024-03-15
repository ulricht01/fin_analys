import requests
from bs4 import BeautifulSoup

def get_rate_usd():
    url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="currency-table")
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        for column in columns:
            if "USD" in column.text:
                exchange_rate = float(columns[4].text.replace(",", "."))
                return exchange_rate

def get_rate_eur():
    url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="currency-table")
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        for column in columns:
            if "EUR" in column.text:
                exchange_rate = float(columns[4].text.replace(",", "."))
                return exchange_rate
            