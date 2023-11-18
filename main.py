import sqlite3
from sqlite3 import Error


# Функція для створення з'єднання до БД 
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


# Вибір таблиці з запиту
def select_table_from_qeury(sql_split, query_type):
    
    if query_type == 'insert':
        query_table = sql_split.index('into') + 1
    elif query_type == 'update':
        query_table = sql_split.index('update') + 1
    else:
        query_table = sql_split.index('from') + 1

    table_name = sql_split[query_table]
    sql = 'SELECT * FROM ' + table_name

    return sql


def execute(conn, sql):
    try:
        # виконання запиту
        cur = conn.cursor()
        cur.execute(sql)

        print('Запит: ' + sql)

        # розділення запиту на окремі слова
        sql_split = sql.lower().split()

        if sql_split[0] == 'select':
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print()
    
        elif sql_split[0] == 'insert':
            print('Запис додано')
            execute(conn, select_table_from_qeury(sql_split, sql_split[0]))

        elif sql_split[0] == 'update' or sql_split[0] == 'delete':
            conn.commit()
            print('Запис змінено / видалено')
            execute(conn, select_table_from_qeury(sql_split, sql_split[0]))

    except Error as e:
        print(e)


# Головна функція, яка виконується під час запуску скрипта
def main():

    # Шлях до БД
    database = r"db.db" 
 
    # Встановлення з'єднання
    conn = create_connection(database)

    # Використовуючи встановлене з'єднання виконуються операції над БД
    with conn:
        print("1. Вивести всі записи з таблиці transactions")
        execute(conn, "SELECT * FROM transactions")

        print("2. Зміна суми транзакції з id = 1 на 150")
        execute(conn, "UPDATE transactions SET amount = 150 WHERE id = 1")

        print("3. Видалення транзакції з id = 2")
        execute(conn, "DELETE FROM transactions WHERE id = 6")

        print("4. Додати нову транзакцію")
        execute(conn, """
                INSERT INTO
                transactions (bill_id, transaction_type_id, amount, comment)
                VALUES (3, 1, 200, 'Нова транзакція');
            """)

        print("5. Вивести всі рахунки з валютою PLN та вивести номер рахунку, ім'я, прізвище, тип валюти та суму залишку для кожного рахунку")
        execute(conn, """
                SELECT bills.id, accounts.surname, accounts.name, currencies.code, bills.residue
                FROM accounts
                JOIN bills ON accounts.id = bills.account_id
                JOIN currencies ON bills.currency_id = currencies.id
                WHERE currencies.code = 'PLN';
            """)
        
 
if __name__ == '__main__':
    main()
