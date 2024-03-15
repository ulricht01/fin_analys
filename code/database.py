import mariadb
from datetime import date

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
        CREATE TABLE IF NOT EXISTS meny (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mena VARCHAR(3),
            czk DOUBLE NOT NULL,
            dt_create DATE NOT NULL DEFAULT CURRENT_DATE
        )
        """)
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

def get_usd():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM meny
        WHERE mena = "USD" and dt_create = %s
        """, (date.today(),)
    )
    usd = cursor.fetchone()
    conn.commit()
    conn.close()
    return usd[0]
    
def get_eur():
    conn, cursor = navaz_spojeni()
    cursor.execute(
        """
        SELECT czk FROM meny
        WHERE mena = "EUR" and dt_create = %s
        """, (date.today(),)
    )
    eur = cursor.fetchone()
    conn.commit()
    conn.close()
    return eur[0]

    