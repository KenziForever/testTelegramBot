from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from db import db_main

admins = ['5354799527']

class fsm_recording(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    photo = State()
    submit = State()


async def is_admin(message: types.Message):
    if str(message.from_user.id) not in admins:
        await message.answer("Ты не администратор.")
        return False
    return True

async def start_record(message: types.Message):
    if await is_admin(message):
        await message.answer('Введите название товара: ')
        await fsm_recording.name.set()

async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введите категорию товара: ')
    await fsm_recording.next()

async def load_category(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Введите размер товара: ')
    await fsm_recording.next()

async def load_size(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Введите цену товара: ')
    await fsm_recording.next()

async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Введите артикул товара: ')
    await fsm_recording.next()

async def load_product_id(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text
    await message.answer('Введите фото товара: ')
    await fsm_recording.next()

async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Верные ли данные: \n'
                f'Название - {data["name"]}\n'
                f'Категория - {data["category"]}\n'
                f'Размер - {data["size"]}\n'
                f'Цена - {data["price"]}\n'
    )
    await message.answer('Верны ли данные?')
    await fsm_recording.submit.set()

async def submit(message: types.Message, state=FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            await db_main.sql_insert_product(
                name=data['name'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )
        await message.answer('Товар добавлен в базу')
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Добавление товара отменено.')
        await state.finish()
    else:
        await message.answer('Ответьте да или нет')

def register_handlers_recording(dp: Dispatcher):
    dp.register_message_handler(start_record, commands=['recording'])
    dp.register_message_handler(load_name, state=fsm_recording.name)
    dp.register_message_handler(load_category, state=fsm_recording.category)
    dp.register_message_handler(load_size, state=fsm_recording.size)
    dp.register_message_handler(load_price, state=fsm_recording.price)
    dp.register_message_handler(load_product_id, state=fsm_recording.product_id)
    dp.register_message_handler(load_photo, state=fsm_recording.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=fsm_recording.submit, content_types=types.ContentType.TEXT)
