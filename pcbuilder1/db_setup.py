import os
import sqlite3

DATABASE = 'pc_parts.db'

def create_connection():
    """Создает подключение к базе данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        print(f"Подключение к базе данных {DATABASE} успешно установлено")
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn


def create_tables(conn):
    """Создание базы данных."""
    try:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cpus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                socket TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS motherboards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                socket TEXT NOT NULL,
                ram_type TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ram (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ram_type TEXT NOT NULL,
                speed INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gpus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                power_consumption INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS power_supplies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                wattage INTEGER NOT NULL
            )
        ''')

        conn.commit()
        print("Таблицы успешно созданы")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")


def populate_tables(conn):
    """Заполняет таблицы тестовыми данными."""
    try:
        cursor = conn.cursor()

        def insert_if_not_exists(table_name, data, columns):
            """Вставляет данные, если они еще не существуют."""
            placeholders = ', '.join(['?'] * len(columns))
            select_query = f"SELECT 1 FROM {table_name} WHERE {' AND '.join([f'{col} = ?' for col in columns])}"
            cursor.execute(select_query, data)
            if cursor.fetchone() is None:  # Запись не существует
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(insert_query, data)
                return True  # Данные вставлены
            return False  # Данные уже существуют

        cpus = [
            ('Intel Core i5-12600K', 'LGA1700'),
            ('AMD Ryzen 5 5600X', 'AM4'),
            ('Intel Core i9-13900K', 'LGA1700'),
            ('AMD Ryzen 9 7950X', 'AM5')
        ]

        for name, socket in cpus:
            if insert_if_not_exists('cpus', (name, socket), ['name', 'socket']):
                print(f"Процессор '{name}' добавлен.")
            else:
                print(f"Процессор '{name}' уже существует.")

        motherboards = [
            ('ASUS ROG Strix Z690-A Gaming WiFi', 'LGA1700', 'DDR5'),
            ('MSI MAG B550 Tomahawk', 'AM4', 'DDR4'),
            ('ASUS ROG Maximus Z790 Hero', 'LGA1700', 'DDR5'),
            ('ASUS ROG Crosshair X670E Hero', 'AM5', 'DDR5')
        ]

        for name, socket, ram_type in motherboards:
            if insert_if_not_exists('motherboards', (name, socket, ram_type), ['name', 'socket', 'ram_type']):
                print(f"Материнская плата '{name}' добавлена.")
            else:
                print(f"Материнская плата '{name}' уже существует.")

        ram = [
            ('Corsair Vengeance LPX 16GB (2x8GB) DDR4 3200MHz', 'DDR4', 3200),
            ('G.Skill Trident Z5 32GB (2x16GB) DDR5 6000MHz', 'DDR5', 6000),
            ('Kingston Fury Beast 16GB (2x8GB) DDR5 5200MHz', 'DDR5', 5200),
            ('Crucial Ballistix 16GB (2x8GB) DDR4 3600MHz', 'DDR4', 3600)
        ]
        for name, ram_type, speed in ram:
            if insert_if_not_exists('ram', (name, ram_type, speed), ['name', 'ram_type', 'speed']):
                print(f"ОЗУ '{name}' добавлена.")
            else:
                print(f"ОЗУ '{name}' уже существует.")

        gpus = [
            ('NVIDIA GeForce RTX 3060', 170),
            ('AMD Radeon RX 6700 XT', 230),
            ('NVIDIA GeForce RTX 4080', 320),
            ('AMD Radeon RX 7900 XTX', 355)
        ]
        for name, power_consumption in gpus:
            if insert_if_not_exists('gpus', (name, power_consumption), ['name', 'power_consumption']):
                print(f"Видеокарта '{name}' добавлена.")
            else:
                print(f"Видеокарта '{name}' уже существует.")

        power_supplies = [
            ('Corsair RM750x (2021)', 750),
            ('Seasonic FOCUS GX-850', 850),
            ('be quiet! Straight Power 11 1000W', 1000),
            ('EVGA SuperNOVA 650 GA', 650)
        ]

        for name, wattage in power_supplies:
            if insert_if_not_exists('power_supplies', (name, wattage), ['name', 'wattage']):
                print(f"Блок питания '{name}' добавлен.")
            else:
                print(f"Блок питания '{name}' уже существует.")

        conn.commit()
        print("Таблицы успешно заполнены данными")

    except sqlite3.Error as e:
        print(f"Ошибка при заполнении таблиц: {e}")


def main():
    # Добавляем удаление базы данных, если она существует
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"Удалена существующая база данных: {DATABASE}")

    conn = create_connection()
    if conn:
        create_tables(conn)
        populate_tables(conn)  # Вызываем populate_tables здесь
        conn.close()
        print("Все операции с базой данных успешно завершены.")
    else:
        print("Не удалось установить соединение с базой данных.")



if __name__ == "__main__":
    main()
