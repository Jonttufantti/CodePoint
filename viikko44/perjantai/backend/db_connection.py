import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tilavaraus"
}

def fetch_users():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM varaajat;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def fetch_tilat():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tilat;")
    tilat = cursor.fetchall()
    cursor.close()
    conn.close()
    return tilat

def fetch_varaukset():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            varaukset.id,
            tilat.tilan_nimi AS tila,
            varaajat.nimi AS varaaja,
            varaukset.varauspaiva
        FROM 
            varaukset
        INNER JOIN 
            tilat ON varaukset.tila = tilat.id
        INNER JOIN 
            varaajat ON varaukset.varaaja = varaajat.id
    """)

    varaukset = cursor.fetchall()

    for varaus in varaukset:
        varaus['varauspaiva'] = varaus['varauspaiva'].strftime('%Y-%m-%d')

    cursor.close()
    conn.close()
    return varaukset
