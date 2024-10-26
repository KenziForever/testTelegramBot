import sqlite3
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM product").fetchall()
    conn.close()
    return products

async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all')
    keyboard.add(button_all)

    await message.answer('Выберите, как отправятся товары:', reply_markup=keyboard)

async def sendall_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название - {product["name"]}\n'  
                       f'Размер - {product["size"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Цена - {product["price"]}\n'
                       f'Артикул - {product["product_id"]}\n\n'
                       f'Фото товара:')

            await callback_query.message.answer_photo(
                photo=product["photo"],
                caption=caption
            )
    else:
        await callback_query.message.answer('Товар не найден')

def register_send_products_handler(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products'])
    dp.register_callback_query_handler(sendall_products, Text(equals='all'))
