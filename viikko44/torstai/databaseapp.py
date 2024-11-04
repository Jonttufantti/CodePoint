import sqlite3
from tabulate import tabulate

def display_tables(cursor):
    SQL_TILAT = "SELECT * FROM tilat"
    SQL_VARAAJAT = "SELECT * FROM varaajat"
    SQL_VARAUKSET = """
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
    """

    # Execute queries and fetch results
    cursor.execute(SQL_TILAT)
    tilat_rows = cursor.fetchall()

    cursor.execute(SQL_VARAAJAT)
    varaajat_rows = cursor.fetchall()

    cursor.execute(SQL_VARAUKSET)
    varaukset_rows = cursor.fetchall()

    # Display tables
    print("\nTilat:")
    print(tabulate(tilat_rows, headers=["ID", "Tilan Nimi"], tablefmt="grid"))

    print("\nVaraajat:")
    print(tabulate(varaajat_rows, headers=["ID", "Nimi"], tablefmt="grid"))

    print("\nVaraukset:")
    print(tabulate(varaukset_rows, headers=["ID", "Tila", "Varaaja", "Varauspäivä"], tablefmt="grid"))

def add_tila(cursor, conn):
    tila_nimi = input("Nimeä uusi tila: ")
    cursor.execute("INSERT INTO tilat (tilan_nimi) VALUES (?)", (tila_nimi,))
    conn.commit()
    print("Uusi tila lisätty.")

def add_varaaja(cursor, conn):
    varaaja_nimi = input("Nimeä uusi varaaja: ")
    cursor.execute("INSERT INTO varaajat (nimi) VALUES (?)", (varaaja_nimi,))
    conn.commit()
    print("Uusi varaaja lisätty.")

def add_varaus(cursor, conn):
    tila_id = input("Syötä tilan ID: ")
    varaaja_id = input("Syötä varaajan ID: ")
    varauspaiva = input("Syötä varauspäivämäärä (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (?, ?, ?)", (tila_id, varaaja_id, varauspaiva))
    conn.commit()
    print("Uusi varaus lisätty.")

def delete_entry(cursor, conn, table_name):
    
    # Check for existing bookings
    if table_name == 'tilat':
        entry_id = input(f"Syötä poistettavan tilan ID: ")
        cursor.execute("SELECT COUNT(*) FROM varaukset WHERE tila = ?", (entry_id,))
        has_booking = cursor.fetchone()[0]
    elif table_name == 'varaajat':
        entry_id = input(f"Syötä poistettavan varaajan ID: ")
        cursor.execute("SELECT COUNT(*) FROM varaukset WHERE varaaja = ?", (entry_id,))
        has_booking = cursor.fetchone()[0]
        print(has_booking)
    elif table_name == 'varaukset':
        entry_id = input(f"Syötä poistettavan varauksen ID: ")
        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entry_id,))
        has_booking = 0

    else:
        print("Taulua ei löytynyt.")
        return

    if has_booking > 0:
        confirm = input(f"This {table_name[:-1]} has existing bookings. Are you sure you want to delete it? (y/n): ")
        if confirm.lower() != 'y':
            print("Poistaminen peruutettu.")
            return
        else:
            # Delete associated bookings first
            cursor.execute("DELETE FROM varaukset WHERE " + ("tila" if table_name == 'tilat' else "varaaja") + " = ?", (entry_id,))
            print(f"All bookings associated with this {table_name[:-1]} have been deleted.")


    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entry_id,))
    conn.commit()
    print(f"{table_name.capitalize()} with ID {entry_id} deleted.")

def main():
    # Establish connection
    conn = sqlite3.connect('my_database.sqlite')
    cursor = conn.cursor()

    while True:
        print("\nVaihtoehdot:")
        print("1. Näytä taulut")
        print("2. Lisää tila")
        print("3. Lisää varaaja")
        print("4. Tee varaus")
        print("5. Poisto tila")
        print("6. Poista varaaja")
        print("7. Poista varaus")
        print("8. Exit")

        choice = input("Tee valinta: ")

        if choice == '1':
            display_tables(cursor)
        elif choice == '2':
            add_tila(cursor, conn)
        elif choice == '3':
            add_varaaja(cursor, conn)
        elif choice == '4':
            add_varaus(cursor, conn)
        elif choice == '5':
            delete_entry(cursor, conn, 'tilat')
        elif choice == '6':
            delete_entry(cursor, conn, 'varaajat')
        elif choice == '7':
            delete_entry(cursor, conn, 'varaukset')
        elif choice == '8':
            break
        else:
            print("Virheellinen valinta. Yritä uudelleen.")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
