import sqlite3
from textual.app import App
from textual.widgets import Button, Static
from tabulate import tabulate

class DatabaseApp(App):
    def __init__(self, database_path: str):
        super().__init__()
        self.database_path = database_path
        self.tables_widget = None  # Initialize tables_widget here

    async def on_mount(self):
        await self.show_tables()

    async def show_tables(self):
        # Connect to the database and fetch data
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        # SQL queries
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

        # Display tables side by side
        tables_display = "\n\n".join([
            "Tilat Table:\n" + tabulate(tilat_rows, headers=["ID", "Tilan Nimi"], tablefmt="grid"),
            "Varaajat Table:\n" + tabulate(varaajat_rows, headers=["ID", "Nimi"], tablefmt="grid"),
            "Varaukset Table:\n" + tabulate(varaukset_rows, headers=["ID", "Tila", "Varaaja", "Varauspäivä"], tablefmt="grid")
        ])

        # Create a Static widget to display tables
        self.tables_widget = Static(tables_display)
        await self.view.dock(self.tables_widget)

        # Create buttons for adding and deleting entries
        add_button = Button("Add Entry", id="add_button")
        delete_button = Button("Delete Entry", id="delete_button")
        await self.view.dock(add_button, edge="bottom")
        await self.view.dock(delete_button, edge="bottom")

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_button":
            await self.add_entry()
        elif event.button.id == "delete_button":
            await self.delete_entry()

    async def add_entry(self):
        # Implement your add entry logic here
        print("Add Entry Button Pressed")
        # For example, you could prompt the user for input
        # and then insert it into the database.

    async def delete_entry(self):
        # Implement your delete entry logic here
        print("Delete Entry Button Pressed")
        # For example, you could ask for the ID of the entry to delete
        # and then remove it from the database.

if __name__ == "__main__":
    app = DatabaseApp("my_database.sqlite")
    app.run()
