# Aplikace pro správu osobních financí

## Cíle aplikace

Cílem této aplikace je vytvořit jednoduché prostředí pro správu osobních financí. Uživatelé budou moci přidávat různé příjmy a výdaje a na základě těchto dat vytvářet jednoduché grafy. Součástí aplikace bude možnost rozdělení transakcí na různé typy zdrojů, jako jsou spořící účty, běžné účty, kryptoměny atd. Dále bude uživatelům zobrazen aktuální kurz eur, dolarů a některých kryptoměn v přepočtu na Kč.

## Použité technologie

1. **Git**: Pro správu verzí a spolupráci na projektu.
2. **Backend s FastAPI**: Pro implementaci backendové části aplikace.
3. **Databázové schéma**: Bude využíváno databázové schéma vytvořené pro MariaDB.
4. **Frontend s HTML, CSS, JavaScriptem**: Pro tvorbu uživatelského rozhraní a interakci s uživatelem. Případně se plánuje naučit základy Reactu pro vytvoření pokročilejšího frontendu.
5. **Docker**: Aplikace bude dockerovaná pro jednoduché nasazení a správu.

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

- **/backend**: Obsahuje backendovou část aplikace napsanou v FastAPI.
- **/frontend**: Obsahuje frontendovou část aplikace, která je vytvořena pomocí HTML, CSS a JavaScriptu.
- **/docs**: Obsahuje dokumentaci aplikace.
- **Dockerfile**: Konfigurace pro vytvoření Docker obrazu.
- **docker-compose.yaml**: Konfigurace pro spuštění aplikace pomocí Docker Compose.

## Dokumentace

Dokumentace aplikace bude k dispozici v adresáři `/docs` a bude obsahovat popis fungování aplikace, návod pro uživatele a UML diagramy.
