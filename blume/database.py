import os

class DatabaseManager:
    def __init__(self):
        self.base_dir = "blume/databases"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_database(self, db_name):
        db_path = os.path.join(self.base_dir, f"{db_name}.txt")
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                pass  # Just create an empty file
            return True
        else:
            print(f"Error: Database '{db_name}' already exists.")
            return False

    def list_databases(self):
        if os.path.exists(self.base_dir):
            return [f.replace('.txt', '') for f in os.listdir(self.base_dir) if f.endswith('.txt')]
        return []

    def database_exists(self, db_name):
        db_path = os.path.join(self.base_dir, f"{db_name}.txt")
        return os.path.exists(db_path)

    def create_table(self, db_name, table_name, columns):
        db_path = os.path.join(self.base_dir, f"{db_name}.txt")
        if not os.path.exists(db_path):
            print(f"Error: Database '{db_name}' does not exist.")
            return False

        with open(db_path, 'r+') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(f"TABLE {table_name}:"):
                    print(f"Error: Table '{table_name}' already exists in database '{db_name}'.")
                    return False

            f.write(f"TABLE {table_name}: {columns}\n")
            return True