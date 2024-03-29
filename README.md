# Aplikace pro správu osobních financí

## Cíle aplikace

Cílem této aplikace je vytvořit jednoduché prostředí pro správu osobních financí. Uživatelé budou moci přidávat různé příjmy a výdaje a sledovat jejich chování pomocí jednoduchých grafů. Součástí aplikace bude možnost rozdělení transakcí na různé typy zdrojů, jako jsou různé typy měn, kryptoměny atd.. Dále bude uživatelům zobrazen aktuální kurz eur, dolarů, liber a některých kryptoměn v přepočtu na Kč.

## Použité technologie

1. **Git**: Pro správu verzí a spolupráci na projektu.
2. **Backend s FastAPI**: Pro implementaci backendové části aplikace.
3. **Databázové schéma**: Bude využíváno databázové schéma vytvořené pro MariaDB.
4. **Frontend s HTML, CSS, JavaScriptem**: Pro tvorbu uživatelského rozhraní a interakci s uživatelem.
5. **Docker**: Aplikace bude dockerizována pro jednoduché nasazení a správu.

## Instalace a spuštění

1. Naklonujte si repozitář:
````
git clone <url-repozitáře>
````

2. Nainstalujte závislosti:
````
pip install -r requirements.txt
````

3. Spusťte aplikaci:
````
uvicorn main:app --reload
````

## Struktura projektu

- **/code**:
 - **/app.py**: Obsahuje backendovou část aplikace, která je vytvořena pomocí FastAPI.
 - **/database.py**: Obsahuje backendovou část aplikace, která obsluhuje databázi.
 - **/app_logic.py**: Obsahuje backendovou část aplikace, která obsahuje některé části logiky aplikace.
 - **/static**: Obsahuje frontendovou část aplikace, která obsahuje JavaScript a css.
 - **/templates**: Obsahuje frontendovou část aplikace, která obsahuje HTML a obrázky.
 - **Dockerfile**: Konfigurace pro vytvoření Docker obrazu.
 - **docker-compose.yaml**: Konfigurace pro spuštění aplikace pomocí Docker Compose.
- **/docs**: Obsahuje dokumentaci aplikace. -> Ještě neexistuje

## Dokumentace

Dokumentace aplikace bude k dispozici v adresáři `/docs` a bude obsahovat popis fungování aplikace, návod pro uživatele a UML diagramy.
