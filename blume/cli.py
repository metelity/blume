import os
import sys
import time
from threading import Thread
from blume.database import DatabaseManager

session_id = 0
start_time = time.time()
version = "1.0.0 realise"

def show_welcome_message():
    print(f"""
Welcome to blume menu database platform.
Metelity Lib Company ©2025

Site - http://185.252.146.112/
Documentation - http://185.252.146.112/docum
Telegram news - https://t.me/metelity

\\h - helper menu
""")

def show_help_menu():
    print("""
Available commands:

CREATE DATABASE <db_name> - Create a new database.
DELETE DATABASE <db_name> - Delete a database.
CREATE TABLE <table_name> <columns> - Create a table in the current database.
SHOW DATABASES - List all databases.
USE <db_name> - Select a database.
TABLE LIST - List all tables in the current database.

Help (\\h) - Show this help menu.
Quit (\\q) - Quit the Blume menu.
Status (\\s) - Show Blume status.
""")

def format_time(seconds):
    days = int(seconds // (24 * 3600))
    seconds %= 24 * 3600
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{days}d, {hours}h, {minutes}m, {int(seconds)}s"

def get_database_count():
    db_dir = "blume/databases"
    if not os.path.exists(db_dir):
        return 0
    return len([f for f in os.listdir(db_dir) if f.endswith('.txt')])

def status():
    uptime = time.time() - start_time
    db_count = get_database_count()
    print(f"""
Status Blume:
- Upd time: {format_time(uptime)}
- Version blume: {version}
- Session id: {session_id}
- Database count: {db_count}
""")

def start_timer():
    while True:
        time.sleep(1)

def delete_database(db_name):
    db_path = os.path.join("blume/databases", f"{db_name}.txt")
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database '{db_name}' deleted successfully.")
    else:
        print(f"Error: Database '{db_name}' does not exist.")

def list_tables(db_name):
    db_path = os.path.join("blume/databases", f"{db_name}.txt")
    if not os.path.exists(db_path):
        print(f"Error: Database '{db_name}' does not exist.")
        return

    with open(db_path, 'r') as f:
        lines = f.readlines()

    tables = set()
    for line in lines:
        if line.startswith("TABLE ") and ":" in line:
            table_name = line.split(":")[0].replace("TABLE ", "").strip()
            if table_name != "TABLE":
                tables.add(table_name)

    if not tables:
        print(f"No tables found in database '{db_name}'.")
    else:
        header = f"{db_name} tables"
        header_length = len(header)
        frame_width = 20
        padding = max(0, frame_width - header_length - 2)

        print("\n┏" + "━" * (frame_width) + "┓")
        print(f"┃ {header}{' ' * padding} ┃")
        print("┡" + "━" * (frame_width) + "┩")
        for index, table_name in enumerate(sorted(tables), start=1):
            print(f"│ {index}. {table_name.ljust(frame_width - 6)}  │")
        print("└" + "─" * (frame_width) + "┘\n")

def create_table(db_name, command):
    db_path = os.path.join("blume/databases", f"{db_name}.txt")
    if not os.path.exists(db_path):
        print(f"Error: Database '{db_name}' does not exist.")
        return False

    table_definitions = command.split(";")
    for table_def in table_definitions:
        table_def = table_def.strip()
        if not table_def:
            continue

        if ":" not in table_def:
            print(f"Error: Invalid table definition. Use 'CREATE TABLE table_name: column1, column2;'")
            return False

        table_name, columns = table_def.split(":", 1)
        table_name = table_name.strip()
        columns = columns.strip()

        if not table_name or not columns:
            print(f"Error: Table name or columns are missing in definition: '{table_def}'")
            return False

        with open(db_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(f"TABLE {table_name}:"):
                    print(f"Error: Table '{table_name}' already exists in database '{db_name}'.")
                    return False

        with open(db_path, 'a') as f:
            f.write(f"TABLE {table_name}: {columns}\n")

        print(f"Table '{table_name}' created successfully in database '{db_name}'.")

    return True

def main():
    global session_id
    session_id += 1
    show_welcome_message()

    timer_thread = Thread(target=start_timer, daemon=True)
    timer_thread.start()

    db_manager = DatabaseManager()
    current_db = None

    while True:
        menu_blume_choice = input("blume> " if not current_db else f"blume ({current_db})> ").strip()

        if menu_blume_choice.upper().startswith("CREATE DATABASE"):
            try:
                db_name = menu_blume_choice.split(" ")[2]
                if len(db_name) < 3:
                    print("Error: Database name must be at least 3 characters long.")
                else:
                    if db_manager.create_database(db_name):
                        print(f"Database '{db_name}' created successfully.")
            except IndexError:
                print("Error: Database name is missing. Usage: CREATE DATABASE <db_name>")

        elif menu_blume_choice.upper().startswith("DELETE DATABASE"):
            try:
                db_name = menu_blume_choice.split(" ")[2]
                delete_database(db_name)
            except IndexError:
                print("Error: Database name is missing. Usage: DELETE DATABASE <db_name>")

        elif menu_blume_choice.upper() == "SHOW DATABASES":
            databases = db_manager.list_databases()
            print("\n┏━━━━━━━━━━━━━━━━━━┓")
            print("┃ Databases        ┃")
            print("┡━━━━━━━━━━━━━━━━━━┩")
            for db in databases:
                print(f"│ {db.ljust(16)} │")
            print("└──────────────────┘\n")

        elif menu_blume_choice.upper().startswith("USE"):
            try:
                if len(menu_blume_choice.split()) == 1:
                    current_db = None
                    print("No database selected.")
                else:
                    db_name = menu_blume_choice.split(" ")[1]
                    if db_manager.database_exists(db_name):
                        current_db = db_name
                        print(f"Using database '{db_name}'.")
                    else:
                        print(f"Error: Database '{db_name}' does not exist.")
            except IndexError:
                print("Error: Database name is missing. Usage: USE <db_name>")

        elif menu_blume_choice.upper() == "TABLE LIST":
            if not current_db:
                print("Error: No database selected. Please use 'USE <db_name>' to select a database.")
            else:
                list_tables(current_db)

        elif menu_blume_choice.upper().startswith("CREATE TABLE"):
            if not current_db:
                print("Error: No database selected. Please use 'USE <db_name>' to select a database.")
            else:
                try:
                    table_definitions = menu_blume_choice[len("CREATE TABLE"):].strip()
                    if not table_definitions:
                        print("Error: Table definitions are missing. Usage: CREATE TABLE table_name: column1, column2;")
                    else:
                        if create_table(current_db, table_definitions):
                            print("Tables created successfully.")
                except Exception as e:
                    print(f"Error: {e}")

        elif menu_blume_choice == "\\h":
            show_help_menu()

        elif menu_blume_choice == "\\s":
            status()

        elif menu_blume_choice == "\\q":
            session_id -= 1
            print("Exiting Blume menu. Goodbye!")
            break

        else:
            print("Unknown command. Type '\\h' for help.")

if __name__ == "__main__":
    main()