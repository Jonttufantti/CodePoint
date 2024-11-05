import mysql.connector
from config.settings import DB_CONFIG




def fetch_users():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM varaajat;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Fetched Users:", users)
    return users

def fetch_tilat():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tilat;")
    tilat = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Fetched rooms:", tilat)
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
    cursor.close()
    conn.close()
    return varaukset
