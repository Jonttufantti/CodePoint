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

def add_tila(tilan_nimi):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tilat (tilan_nimi) VALUES (%s)", (tilan_nimi,))
    conn.commit()
    cursor.close()
    conn.close()

def add_varaaja(nimi):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO varaajat (nimi) VALUES (%s)", (nimi,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_tila(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    # Check if there are any existing varaukset for the tila
    cursor.execute("SELECT COUNT(*) FROM varaukset WHERE tila = %s", (id,))
    count = cursor.fetchone()[0]
    if count > 0:
        return "Warning: Deleting this tila will also delete any associated varaus."
    cursor.execute("DELETE FROM tilat WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return None

def delete_varaaja(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    # Check if there are any existing varaukset for the varaaja
    cursor.execute("SELECT COUNT(*) FROM varaukset WHERE varaaja = %s", (id,))
    count = cursor.fetchone()[0]
    if count > 0:
        return "Warning: Deleting this varaaja will also delete any associated varaus."
    cursor.execute("DELETE FROM varaajat WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return None
