import sqlite3
from db import queris

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('База данных подключена')
    cursor.execute(queris.CREATE_TABLE_PRODUCT)
    db.commit()

async def sql_insert_product(name, category, size, price, product_id, photo):
    cursor.execute(queris.INSERT_PRODUCT_QUERY, (
        name, category, size, price, product_id, photo
    ))
    db.commit()
