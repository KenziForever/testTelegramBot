from aiogram import types, Dispatcher
import os
from config import bot

async def commands_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Добро пожалавать {name} чем могу помочь?')

async def commands_info(message: types.Message):
    await message.answer('Инфо про бота:\n'
                         'Этот бот помогает сотрудникам добавлять товары и управлять заказами клиентов.\n'
                         'Вы можете использовать команды для просмотра доступных товаров и оформления заказов.\n')

def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_info, commands=['info'])