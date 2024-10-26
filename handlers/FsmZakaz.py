from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import Stuff, token

bot = Bot(token=token)

class fsm_zakaz(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    contact_info = State()

async def start_zakaz(message: types.Message):
    await message.answer('Введите артикул товара, который хотите купить:')
    await fsm_zakaz.product_id.set()

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text
    await message.answer('Введите размер товара:')
    await fsm_zakaz.size.set()

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Введите количество товара:')
    await fsm_zakaz.quantity.set()

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await message.answer('Введите ваши контактные данные:')
    await fsm_zakaz.contact_info.set()

async def load_contact_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact_info'] = message.text

    zakaz_message = (f'Новый заказ:\n'
                     f'Артикул: {data["product_id"]}\n'
                     f'Размер: {data["size"]}\n'
                     f'Количество: {data["quantity"]}\n'
                     f'Контактные данные: {data["contact_info"]}\n')

    for staff_id in Stuff:
        await bot.send_message(chat_id=staff_id, text=zakaz_message)

    await message.answer('Ваш заказ принят ')
    await state.finish()

def register_zakaz_handlers(dp: Dispatcher):
    dp.register_message_handler(start_zakaz, commands=['zakaz'])
    dp.register_message_handler(load_product_id, state=fsm_zakaz.product_id)
    dp.register_message_handler(load_size, state=fsm_zakaz.size)
    dp.register_message_handler(load_quantity, state=fsm_zakaz.quantity)
    dp.register_message_handler(load_contact_info, state=fsm_zakaz.contact_info)
