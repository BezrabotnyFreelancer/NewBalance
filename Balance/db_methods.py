import sqlite3
import datetime
from enum import Enum


class Scope(Enum):
    ALL = 1
    SUM = 2
    COUNT = 3
    AVG = 4


db_name = 'Balance/Balance.db'


def validate_member(id, firstname, lastname):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS MEMBER(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), FIRST_NAME VARCHAR(50), LAST_NAME VARCHAR(50))')
    conn.commit()

    # Select our user id for find hin in our table
    cursor.execute(f'SELECT USER_ID FROM MEMBER WHERE USER_ID = {id}')

    if cursor.fetchone() is None:
        # Add user in table
        cursor.execute('INSERT INTO MEMBER (USER_ID, FIRST_NAME, LAST_NAME) VALUES (?,?,?)',
                       (id, firstname, lastname))
        conn.commit()

    conn.close()


def insert_data(table_name, data, user):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    date = datetime.date.today()
    cursor.execute(f'INSERT INTO {table_name}(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (user, data, date))
    conn.commit()
    conn.close()


operations = {
    Scope.ALL.name: '*',
    Scope.SUM.name: 'SUM(TOTAL)',
    Scope.COUNT.name: 'COUNT(TOTAL)',
    Scope.AVG.name: 'AVG(TOTAL)'
}


def get_data(user, table_name: str, operation, interval: int):
    try:
        scope = operations[operation]
    except KeyError:
        raise Exception('Not supported operation')
    filter = f'AND "DATE" BETWEEN DATETIME("now", "-{interval} month") AND DATETIME("now", "localtime") ORDER BY "DATE"' if int(
        interval) > 0 else ''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {scope} FROM {table_name} WHERE USER_ID = {user} {filter}')
    data = round(cursor.fetchone()[0], 2) if operation != Scope.ALL.name else cursor.fetchall()
    conn.close()
    return data