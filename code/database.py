import mariadb
from datetime import date, datetime

def navaz_spojeni():
    config = {
        "user": "root",
        "password": "secret",
        "host": "localhost",
        "port": 3306,
        "database": "fin_db",
    }
    conn = mariadb.connect(**config)
    cursor = conn.cursor()
    return conn,cursor

def vytvor_tabulky():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS uzivatele (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(70),
            uzivatel VARCHAR(25),
            heslo VARCHAR(70),
            dt_create DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS meny (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mena ENUM("CZK", "USD", "EUR", "GBP", "SHIB", "BITC", "DOGE"),
            czk DOUBLE NOT NULL,
            dt_create DATE NOT NULL DEFAULT CURRENT_DATE
        );
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prijmy (
            id INT AUTO_INCREMENT PRIMARY KEY,
            prijem DOUBLE,
            prijem_CZK DOUBLE,
            mena VARCHAR(4),
            datum DATE,
            cas TIME,
            kategorie ENUM("Výplata", "Alimenty", "Kapesné", "Dar", "Podnikání", "Ostatní"),
            id_uzivatel INT NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT `fk_prijmy_uzivatele`
                FOREIGN KEY (id_uzivatel) REFERENCES uzivatele (id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT
        );
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vydaje (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vydaj DOUBLE,
            vydaj_CZK DOUBLE,
            mena VARCHAR(4),
            datum DATE,
            cas TIME,
            kategorie ENUM("Nájem", "Elektřina", "Internet", "Mobilní tarif", "Pojištění", "Potraviny", "Ostatní"),
            id_uzivatel INT NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT `fk_vydaje_uzivatele`
                FOREIGN KEY (id_uzivatel) REFERENCES uzivatele (id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT
        );
        """)
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id VARCHAR(255) PRIMARY KEY,
            id_uzivatel INT NOT NULL,
            vytvoreno DATETIME DEFAULT CURRENT_TIMESTAMP,
            posledni_aktivita DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT `fk_sessions_uzivatele`
                FOREIGN KEY (id_uzivatel) REFERENCES uzivatele (id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT
        );
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ucty (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_uzivatel INT NOT NULL,
            dt_zapis DATE,
            zustatek DOUBLE DEFAULT 0,
            typ ENUM("Příjem", "Výdaj"),
            cas TIME,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT `fk_ucty_uzivatele`
                FOREIGN KEY (id_uzivatel) REFERENCES uzivatele (id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT
        );
        """)
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS krypto (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mena ENUM("SHIB", "BITC", "DOGE"),
            czk DOUBLE NOT NULL,
            dt_create DATE NOT NULL DEFAULT CURRENT_DATE,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)
    conn.commit()
    conn.close()
    
def pridej_uzivatele_do_db(mail, uzivatel, heslo):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        INSERT INTO uzivatele (email, uzivatel, heslo)
        VALUES (%s, %s, %s)
        """, (mail, uzivatel, heslo)
    )
    conn.commit()
    conn.close()
    
    
def pridej_prijem_do_db(prijem, mena, datum, cas, kategorie, id_uzivatel):
    kurzy = {
        "USD": get_usd(datum),
        "EUR": get_eur(datum),
        "GBP": get_gbp(datum),
        "SHIB" : get_shiba(datum),
        "BITC" : get_bitcoin(datum),
        "DOGE" : get_doge(datum),
        "CZK": 1  # Kurz pro CZK je vždy 1
    }
    kurz = kurzy.get(mena)

    prijem_czk = float(prijem) * kurz
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        INSERT INTO prijmy (prijem, prijem_czk, mena, datum, cas, kategorie, id_uzivatel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (prijem, prijem_czk, mena, datum, cas, kategorie, id_uzivatel)
    )
    
    cursor.execute(
        """
        INSERT INTO ucty (id_uzivatel, dt_zapis, cas, zustatek, typ)
        VALUES (%s, %s, %s, %s,"Příjem")
        """, (id_uzivatel, datum, cas, prijem_czk)
    )
    conn.commit()
    conn.close()
    
def pridej_vydaj_do_db(vydaj, mena, datum, cas, kategorie, id_uzivatel):
    kurzy = {
        "USD": get_usd(datum),
        "EUR": get_eur(datum),
        "GBP": get_gbp(datum),
        "SHIB" : get_shiba(datum),
        "BITC" : get_bitcoin(datum),
        "DOGE" : get_doge(datum),
        "CZK": 1  # Kurz pro CZK je vždy 1
    }
    
    kurz = kurzy.get(mena)
    vydaj_czk = float(vydaj) * kurz
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        INSERT INTO vydaje (vydaj, vydaj_czk, mena, datum, cas, kategorie, id_uzivatel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (vydaj, vydaj_czk, mena, datum, cas, kategorie, id_uzivatel)
    )
    
    cursor.execute(
        """
        INSERT INTO ucty (id_uzivatel, dt_zapis, cas, zustatek, typ)
        VALUES (%s, %s, %s,%s, "Výdaj")
        """, (id_uzivatel, datum, cas, -vydaj_czk)
    )
    conn.commit()
    conn.close()
    
def pridej_kurz_do_db(mena, czk):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT dt_create FROM meny
        WHERE mena = %s and dt_create = %s
        """, (mena, date.today(),)
    )
    today_hodnota = cursor.fetchone()
    
    if today_hodnota == None:
        cursor.execute(
            """
            INSERT INTO meny (mena, czk) 
            VALUES (%s, %s)
            """, (mena, czk)
            )
        conn.commit()
        conn.close()
    else:
        pass

def get_usd(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM meny
        WHERE mena = "USD" and dt_create >= %s
        ORDER BY dt_create asc
        """, (datum,)
    )
    usd = cursor.fetchone()
    conn.commit()
    conn.close()
    return usd[0]

def get_eur(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM meny
        WHERE mena = "EUR" and dt_create >= %s
        ORDER BY dt_create asc
        """, (datum,)
    )
    eur = cursor.fetchone()
    conn.commit()
    conn.close()
    return eur[0]

def get_gbp(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM meny
        WHERE mena = "GBP" and dt_create >= %s
        """, (datum,)
    )
    gbp = cursor.fetchone()
    conn.commit()
    conn.close()
    return gbp[0]

def heslo_check(uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
    """
    SELECT heslo FROM uzivatele
    WHERE uzivatel = %s
    """, (uzivatel,))
    heslo = cursor.fetchone()
    conn.commit()
    conn.close()
    return heslo[0]

def uzivatel_check(uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
    """
    SELECT uzivatel FROM uzivatele
    WHERE uzivatel = %s
    """, (uzivatel,))
    uzivatel = cursor.fetchone()
    conn.commit()
    conn.close()
    if uzivatel == None:
        return None
    else:
        return uzivatel[0]

def mail_check(mail):
    conn, cursor = navaz_spojeni()
    cursor.execute(
    """
    SELECT email FROM uzivatele
    WHERE email = %s
    """, (mail,))
    mail = cursor.fetchone()
    conn.commit()
    conn.close()
    if mail == None:
        return None
    else:
        return mail[0]
    
def get_user_id(username):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id FROM uzivatele
        WHERE uzivatel = %s
        """, (username,))
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    if user == None:
        return None
    else:
        return user[0]
    
def pridej_session(id, id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        INSERT INTO sessions (id, id_uzivatel)
        VALUES (%s, %s)
        """, (id, id_uzivatel)
        )
    conn.commit()
    conn.close()


def odeber_session(id_session):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        DELETE FROM sessions
        WHERE id= %s
        """, (id_session,)
        )
    conn.commit()
    conn.close()

def aktualizuj_session(id_session):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        UPDATE sessions
        SET posledni_aktivita = %s
        WHERE id = %s
        """, (datetime.now(), id_session,)
        )
    conn.commit()
    conn.close()

def select_session(session_id):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id FROM sessions
        WHERE id = %s
        """, (session_id,))
    session_res = cursor.fetchone()
    conn.commit()
    conn.close()
    if session_res == None:
        return None
    else:
        return session_res[0]
    
def get_session_id(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id FROM sessions
        WHERE id_uzivatel = %s
        """, (id_uzivatel,))
    session_id = cursor.fetchone()
    conn.commit()
    conn.close()
    if session_id == None:
        return None
    else:
        return session_id[0]
    
def get_user_id_via_session(session_id):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id_uzivatel from sessions
        WHERE id = %s
        """, (session_id,)
    )
    uzivatel_id = cursor.fetchone()
    conn.commit()
    conn.close()
    return uzivatel_id[0]
    

def prijmy_pie_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT kategorie, sum(prijem_czk) as prijem FROM prijmy
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def prijmy_bar_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(datum, '%d.%m.%Y') AS datum, sum(prijem_czk) as prijem FROM prijmy
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def prijmy_month_bar_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT concat(year(datum), "/", month(datum)), sum(prijem_czk) as prijem FROM prijmy
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def vydaje_pie_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT kategorie, sum(vydaj_czk) as vydaj FROM vydaje
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def vydaje_bar_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(datum, '%d.%m.%Y') AS datum, sum(vydaj_czk) as vydaj FROM vydaje
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def vydaje_month_bar_data(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT concat(year(datum), "/", month(datum)), sum(vydaj_czk) as vydaj FROM vydaje
        WHERE id_uzivatel = %s
        GROUP BY 1
        """, (id_uzivatel,)
    )
    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return {"labels": labels, "data": values}

def nacti_eur_kurzy_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, czk FROM meny
        WHERE mena = 'EUR'
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def nacti_usd_kurzy_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, czk FROM meny
        WHERE mena = 'USD'
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def nacti_gbp_kurzy_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, czk FROM meny
        WHERE mena = 'GBP'
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def kategorie_prijmy():
    conn, cursor = navaz_spojeni()
    cursor.execute("DESCRIBE prijmy")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in results:
        if row[0] == 'kategorie':
            enum_values_str = row[1]
            enum_values = enum_values_str[enum_values_str.find("(")+1:enum_values_str.find(")")]
            enum_values = enum_values.replace("'", "")
            enum_values = enum_values.split(",")
            return enum_values
    return "No results found."

def kategorie_vydaje():
    conn, cursor = navaz_spojeni()
    cursor.execute("DESCRIBE vydaje")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in results:
        if row[0] == 'kategorie':
            enum_values_str = row[1]
            enum_values = enum_values_str[enum_values_str.find("(")+1:enum_values_str.find(")")]
            enum_values = enum_values.replace("'", "")
            enum_values = enum_values.split(",")
            return enum_values
    return "No results found."

def get_all_sessions():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT * from sessions
        """
    )
    columns = [column[0] for column in cursor.description]  # Získání názvů sloupců
    sessions = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Přeformátování výsledku do slovníku
    conn.commit()
    conn.close()
    return sessions
    
def volby_meny():
    conn, cursor = navaz_spojeni()
    cursor.execute("DESCRIBE meny")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in results:
        if row[0] == 'mena':
            enum_values_str = row[1]
            enum_values = enum_values_str[enum_values_str.find("(")+1:enum_values_str.find(")")]
            enum_values = enum_values.replace("'", "")
            enum_values = enum_values.split(",")
            return enum_values
    return "No results found."

def zustatky(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DISTINCT
            DATE_FORMAT(dt_zapis, '%d.%m.%Y') AS datum,
            SUM(zustatek) OVER (ORDER BY dt_zapis) AS kumulativni_zustatek
        FROM ucty
        WHERE id_uzivatel = %s
        ORDER BY dt_zapis
        """,
        (id_uzivatel,)
    )
    data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    datumy = [row[0] for row in data]
    zustatky = [row[1] for row in data]
        
    return {"datumy": datumy, "zustatky": zustatky}

def zustatky_bar(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT
            DATE_FORMAT(dt_zapis, '%d.%m.%Y') AS datum,
            SUM(CASE WHEN typ = 'Příjem' THEN zustatek ELSE 0 END) AS prijem,
            SUM(CASE WHEN typ = 'Výdaj' THEN -zustatek ELSE 0 END) AS vydej
        FROM ucty
        WHERE id_uzivatel = %s
        GROUP BY 1
        ORDER BY dt_zapis
        """,
        (id_uzivatel,)
    )
    data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    datumy = [row[0] for row in data]
    prijem = [row[1] for row in data]
    vydej = [row[2] for row in data]
        
    return {"datumy": datumy, "prijem": prijem, "vydej": vydej}

def pridej_krypto_do_db(mena, krypto):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        INSERT INTO krypto (mena, czk)
        VALUES (%s, %s)
        """, (mena,krypto)
    )
    
    cursor.execute(
        """
        DELETE FROM meny
        WHERE mena = %s and dt_create = %s
        """, (mena, date.today())
    )
    
    cursor.execute(
        """
        INSERT INTO meny (mena, czk, dt_create)
        VALUES(%s, %s, %s)
        """, (mena, krypto, date.today())
    )
    
    conn.commit()
    conn.close()


def nacti_bitc_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, avg(czk) as czk 
        FROM krypto
        WHERE mena = 'BITC'
        GROUP BY 1
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def nacti_shiba_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, avg(czk) as czk 
        FROM krypto
        WHERE mena = 'SHIB'
        GROUP BY 1
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def nacti_doge_line():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT DATE_FORMAT(dt_create, '%d.%m.%Y') AS datum, avg(czk) as czk 
        FROM krypto
        WHERE mena = 'DOGE'
        GROUP BY 1
        """
    )
    data = cursor.fetchall()
    conn.close()

    datumy = []
    koruny = []
    for row in data:
        datumy.append(row[0])
        koruny.append(row[1])

    return {"datumy": datumy, "koruny": koruny}

def get_shiba(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM krypto
        WHERE mena = "SHIB" and dt_create >= %s
        ORDER BY dt_create ASC, time DESC
        """, (datum,)
    )
    shiba = cursor.fetchone()
    conn.commit()
    conn.close()
    return shiba[0]
    
def get_bitcoin(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM krypto
        WHERE mena = "BITC" and dt_create >= %s
        ORDER BY dt_create ASC, time DESC
        """, (datum,)
    )
    bitcoin = cursor.fetchone()
    conn.commit()
    conn.close()
    return bitcoin[0]

def get_doge(datum):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM krypto
        WHERE mena = "DOGE" and dt_create >= %s
        ORDER BY dt_create ASC, time DESC
        """, (datum,)
    )
    doge = cursor.fetchone()
    conn.commit()
    conn.close()
    return doge[0]

def prijem_nacti_ccy_pie():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT mena, sum(prijem_czk) as prijem FROM prijmy
        GROUP BY 1
        """,
    )
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    ccy = []
    czk = []
    
    for row in data: 
        ccy.append(row[0])
        czk.append(row[1])
    
    return {"ccy": ccy, "czk": czk }

def vyd_nacti_ccy_pie_data():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT mena, sum(vydaj_czk) as vydaj FROM vydaje
        GROUP BY 1
        """,
    )
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    ccy = []
    czk = []
    
    for row in data: 
        ccy.append(row[0])
        czk.append(row[1])
    
    return {"ccy": ccy, "czk": czk }

def nacti_souhrn_pie():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT typ, sum(abs(zustatek)) as vydaj FROM ucty
        GROUP BY 1
        """,
    )
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    labels = []
    czk = []
    
    for row in data: 
        labels.append(row[0])
        czk.append(row[1])
    
    return {"labels": labels, "czk": czk }

def zustatky_bar_monthly(id_uzivatel):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT
            CONCAT(YEAR(dt_zapis), "/", MONTH(dt_zapis)) AS datum,
            SUM(CASE WHEN typ = 'Příjem' THEN zustatek ELSE 0 END) AS prijem,
            SUM(CASE WHEN typ = 'Výdaj' THEN -zustatek ELSE 0 END) AS vydej
        FROM ucty
        WHERE id_uzivatel = %s
        GROUP BY 1
        ORDER BY dt_zapis
        """,
        (id_uzivatel,)
    )
    data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    datumy = [row[0] for row in data]
    prijem = [row[1] for row in data]
    vydej = [row[2] for row in data]
        
    return {"datumy": datumy, "prijem": prijem, "vydej": vydej}

def nacti_prijmy_pro_tab(id_uzivatele):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id, prijem_CZK, mena, datum, DATE_FORMAT(cas, '%H:%i') AS cas, kategorie FROM prijmy
        WHERE id_uzivatel = %s
        ORDER BY datum, cas
        """, (id_uzivatele,)
    )
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    
    ids = []
    prijmy = []
    meny = []
    datumy = []
    casy = []
    kategorie = []
    for row in data:
        ids.append(row[0])
        prijmy.append(row[1])
        meny.append(row[2])
        datumy.append(row[3])
        casy.append(row[4])
        kategorie.append(row[5])
        
    return {"ids" : ids,
            "prijmy" : prijmy,
            "meny" : meny,
            "datumy" : datumy,
            "casy" : casy,
            "kategorie" : kategorie}


def smaz_prijem(id):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT datum, cas, id_uzivatel, time
        FROM prijmy
        WHERE id = %s
        """, (id,)
    )
    result = cursor.fetchone()

    datum, cas, id_uzivatel, zapis = result[0], result[1], result[2], result[3]
    
    cursor.execute(
        """
        DELETE FROM prijmy
        WHERE id = %s
        """, (id,)
    )
    
    cursor.execute(
        """
        DELETE FROM ucty
        WHERE id_uzivatel = %s and cas = %s and dt_zapis = %s and time = %s
        """, (id_uzivatel, cas, datum, zapis)
    )
    conn.commit()
    conn.close()
    



def nacti_vydaje_pro_tab(id_uzivatele):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT id, vydaj_CZK, mena, datum, DATE_FORMAT(cas, '%H:%i') AS cas, kategorie FROM vydaje
        WHERE id_uzivatel = %s
        ORDER BY datum, cas
        """, (id_uzivatele,)
    )
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    
    ids = []
    vydaje = []
    meny = []
    datumy = []
    casy = []
    kategorie = []
    for row in data:
        ids.append(row[0])
        vydaje.append(row[1])
        meny.append(row[2])
        datumy.append(row[3])
        casy.append(row[4])
        kategorie.append(row[5])
        
    return {"ids" : ids,
            "vydaje" : vydaje,
            "meny" : meny,
            "datumy" : datumy,
            "casy" : casy,
            "kategorie" : kategorie}


def smaz_vydaj(id):
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT datum, cas, id_uzivatel, time
        FROM vydaje
        WHERE id = %s
        """, (id,)
    )
    result = cursor.fetchone()
    
    datum, cas, id_uzivatel, zapis = result[0], result[1], result[2], result[3]
    
    cursor.execute(
        """
        DELETE FROM vydaje
        WHERE id = %s
        """, (id,)
    )
    
    cursor.execute(
        """
        DELETE FROM ucty
        WHERE id_uzivatel = %s and cas = %s and dt_zapis = %s and time = %s
        """, (id_uzivatel, cas, datum, zapis)
    )
    conn.commit()
    conn.close()