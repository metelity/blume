import os

class Connect:
    def __init__(self):
        self.database = None
        self.base_dir = "blume/databases"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_database(self, db_name):
        """
        Создает новую базу данных, если она не существует.
        :param db_name: Имя базы данных.
        """
        db_path = os.path.join(self.base_dir, f"{db_name}.txt")
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                pass  # Создаем пустой файл
            print(f"База данных '{db_name}' создана.")
            return True
        else:
            print(f"База данных '{db_name}' уже существует.")
            return False

    def set_database(self, db_name):
        """
        Подключается к указанной базе данных.
        :param db_name: Имя базы данных.
        """
        db_path = os.path.join(self.base_dir, f"{db_name}.txt")
        if not os.path.exists(db_path):
            print(f"Ошибка: База данных '{db_name}' не существует.")
            return False
        self.database = db_name
        print(f"Используется база данных '{db_name}'.")
        return True

    def create_table(self, table_name, columns):
        """
        Создает таблицу в текущей базе данных.
        :param table_name: Имя таблицы.
        :param columns: Строка с названиями столбцов, разделенными запятыми.
        """
        if not self.database:
            print("Ошибка: База данных не выбрана. Используйте 'set_database' для выбора базы данных.")
            return False

        db_path = os.path.join(self.base_dir, f"{self.database}.txt")
        if not os.path.exists(db_path):
            print(f"Ошибка: База данных '{self.database}' не существует.")
            return False

        with open(db_path, 'r+') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(f"TABLE {table_name}:"):
                    print(f"Ошибка: Таблица '{table_name}' уже существует в базе данных '{self.database}'.")
                    return False

            f.write(f"TABLE {table_name}: {columns}\n")
            print(f"Таблица '{table_name}' создана в базе данных '{self.database}'.")
            return True

    def list_tables(self):
        """
        Возвращает список всех таблиц в текущей базе данных.
        """
        if not self.database:
            print("Ошибка: База данных не выбрана. Используйте 'set_database' для выбора базы данных.")
            return []

        db_path = os.path.join(self.base_dir, f"{self.database}.txt")
        if not os.path.exists(db_path):
            print(f"Ошибка: База данных '{self.database}' не существует.")
            return []

        tables = []
        with open(db_path, 'r') as f:
            for line in f:
                if line.startswith("TABLE "):
                    table_name = line.split(":")[0].replace("TABLE ", "").strip()
                    tables.append(table_name)
        return tables

    def drop_table(self, table_name):
        """
        Удаляет таблицу из текущей базы данных.
        :param table_name: Имя таблицы.
        """
        if not self.database:
            print("Ошибка: База данных не выбрана. Используйте 'set_database' для выбора базы данных.")
            return False

        db_path = os.path.join(self.base_dir, f"{self.database}.txt")
        if not os.path.exists(db_path):
            print(f"Ошибка: База данных '{self.database}' не существует.")
            return False

        with open(db_path, 'r') as f:
            lines = f.readlines()

        with open(db_path, 'w') as f:
            deleted = False
            for line in lines:
                if not line.startswith(f"TABLE {table_name}:"):
                    f.write(line)
                else:
                    deleted = True

            if deleted:
                print(f"Таблица '{table_name}' удалена из базы данных '{self.database}'.")
            else:
                print(f"Ошибка: Таблица '{table_name}' не существует в базе данных '{self.database}'.")
            return deleted

# Глобальный объект для удобства
Connect.blume = Connect()