import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tilavaraus"
}

def verify_user(username, password):
    connection = mysql.connector.connect(
        host=DB_CONFIG["host"], 
        user=DB_CONFIG["user"], 
        password=DB_CONFIG["password"], 
        database=DB_CONFIG["database"]
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kayttajat WHERE nimi = %s AND salasana = %s", (username, password))
    user = cursor.fetchone()

    print("Queried user:", user)
    print("Username:", username)
    print("Password:", password)

    # Check if user exists and passwords match
    if user and user['salasana'] == password:
        return user
    return None

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

def add_varaus(tila_id, varaaja_id, varauspaiva):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (%s, %s, %s)",
        (tila_id, varaaja_id, varauspaiva)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_tila(id, force=False):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM varaukset WHERE tila = %s", (id,))
    count = cursor.fetchone()[0]

    if count > 0 and not force:
        cursor.close()
        conn.close()
        return "Varoitus: Poistamalla tämän tilan, poistat myös sen varaukset."  
    elif force:
        cursor.execute("DELETE FROM varaukset WHERE tila = %s", (id,))
    
    cursor.execute("DELETE FROM tilat WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return None


def delete_varaaja(id, force=False):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM varaukset WHERE varaaja = %s", (id,))
    count = cursor.fetchone()[0]

    if count > 0 and not force:
        cursor.close()
        conn.close()
        return "Varoitus: Poistamalla tämän varaajan, poistat myös hänen varaukset."
    elif force:
        cursor.execute("DELETE FROM varaukset WHERE varaaja = %s", (id,))
    
    cursor.execute("DELETE FROM varaajat WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return None

def delete_varaus(varaus_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Check for existing bookings (varaus)
    cursor.execute("SELECT COUNT(*) FROM varaukset WHERE id = %s", (varaus_id,))
    has_booking = cursor.fetchone()[0]

    if has_booking > 0:
        # Proceed with deleting the varaus if it exists
        cursor.execute("DELETE FROM varaukset WHERE id = %s", (varaus_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Successfully deleted varaus
    else:
        cursor.close()
        conn.close()
        return False  # No varaus found
