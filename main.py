from aiogram import executor
import logging
from config import dp
from handlers import commands, FSM_recording, Send_Products, FsmZakaz
from db import db_main

FSM_recording.register_handlers_recording(dp)
Send_Products.register_send_products_handler(dp)
FsmZakaz.register_zakaz_handlers(dp)
commands.register_handlers_commands(dp)

async def on_startup(_):
    await db_main.sql_create()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)