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
    print("\nTilat Table:")
    print(tabulate(tilat_rows, headers=["ID", "Tilan Nimi"], tablefmt="grid"))

    print("\nVaraajat Table:")
    print(tabulate(varaajat_rows, headers=["ID", "Nimi"], tablefmt="grid"))

    print("\nVaraukset Table:")
    print(tabulate(varaukset_rows, headers=["ID", "Tila", "Varaaja", "Varauspäivä"], tablefmt="grid"))

def add_tila(cursor, conn):
    tila_nimi = input("Enter the name of the new tila: ")
    cursor.execute("INSERT INTO tilat (tilan_nimi) VALUES (?)", (tila_nimi,))
    conn.commit()
    print("New tila added.")

def add_varaaja(cursor, conn):
    varaaja_nimi = input("Enter the name of the new varaaja: ")
    cursor.execute("INSERT INTO varaajat (nimi) VALUES (?)", (varaaja_nimi,))
    conn.commit()
    print("New varaaja added.")

def add_varaus(cursor, conn):
    tila_id = input("Enter the ID of the tila: ")
    varaaja_id = input("Enter the ID of the varaaja: ")
    varauspaiva = input("Enter the reservation date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (?, ?, ?)", (tila_id, varaaja_id, varauspaiva))
    conn.commit()
    print("New varaus added.")

def delete_entry(cursor, conn, table_name):
    entry_id = input(f"Enter the ID of the {table_name} to delete: ")

    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entry_id,))
    conn.commit()
    print(f"{table_name.capitalize()} with ID {entry_id} deleted.")

def main():
    # Establish connection
    conn = sqlite3.connect('my_database.sqlite')
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Display Tables")
        print("2. Add Tila")
        print("3. Add Varaaja")
        print("4. Add Varauksen")
        print("5. Delete Tila")
        print("6. Delete Varaaja")
        print("7. Delete Varauksen")
        print("8. Exit")

        choice = input("Enter your choice: ")

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
            print("Invalid choice. Please try again.")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
