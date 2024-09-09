
import os 

import datetime
import subprocess

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup ,KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '6762242611:AAGtUAMrpmzQwQgxYsjF_Iu5RqlyZkF6SDo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

numbers = [i.split('.')[0] for i in os.listdir() if i.endswith('.session')]

update_keys = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('Vaqt'),
                KeyboardButton('Matn'),
            ],
            [
                KeyboardButton("gurux qo'shish"),
                KeyboardButton("gurux o'chirish"),
            ],
            [
                KeyboardButton("O'chirish"),
                KeyboardButton("Yoqish")
            ],

        ],resize_keyboard=True
    )


def number_buttons():
    numbers = [i.split('.')[0] for i in os.listdir() if i.endswith('.session')]
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(i)
            ] for i in numbers
        ]
    )

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state:FSMContext):
    await state.set_state("select_number")
    await message.answer('Raqamni tanlang.', reply_markup=number_buttons())


@dp.message_handler(content_types="text", state="select_number")
async def update(message:types.Message, state:FSMContext):
    if message.text in numbers:
        await state.set_data({'session':message.text})
        await state.set_state('update_anything')
        await message.answer("Nimani o'zgartiramiz", reply_markup=update_keys)
    else:
        await message.answer("Tugmalar orqani tanlang.")


@dp.message_handler(text="O'chirish", state='*')
async def down(message, state):
    data = await state.get_data()
    session = data.get('session').split('.')[0]
    subprocess.check_output(f"systemctl stop {session}", shell=True)
    await state.set_state("select_number")
    await message.answer(f"{session} O'chirildi", reply_markup=number_buttons())

@dp.message_handler(text="Yoqish", state='*')
async def down(message, state):
    data = await state.get_data()
    session = data.get('session').split('.')[0]
    print(f"systemctl start {session}")
    subprocess.check_output(f"systemctl start {session}", shell=True)
    await state.set_state("select_number")
    await message.answer(f"{session} yoqildi", reply_markup=number_buttons())

@dp.message_handler(lambda msg: msg.text in ["Vaqt", "gurux qo'shish","gurux o'chirish", "Matn"], state="update_anything")
async def update_anything(message:types.Message, state:FSMContext):
    await state.set_state(f"updating_{message.text}")
    await state.update_data({"updating":message.text})
    if message.text == "gurux o'chirish":
        with open('groups.txt') as groups:
            await message.answer(groups.read())

    await message.answer(f"{message.text} uchun yangi qiymat kiriting")

@dp.message_handler(state='*')
async def update_time(message:types.Message, state:FSMContext):
    data = await state.get_data()
    session = data.pop('session').split('.')[0]
    updating = data.pop("updating")

    if updating.lower() == "gurux qo'shish":
        with open('groups.txt','a+') as groups:
            groups.write(f'-100{message.text}\n')
        await message.answer(f"gurux ro'yhatga qo'shildi", reply_markup=number_buttons())
    elif updating.lower() == "gurux o'chirish":
        with open('groups.txt') as groups:
            groupstxt = groups.read()
        with open('groups.txt','w') as groups:
            groups.write(groupstxt.replace(f'-100{message.text}\n',''))
    elif updating.lower() == "vaqt":
        with open(f"{session}{updating.lower()}.txt","w") as time:
            delta = datetime.timedelta(minutes=int(message.text))
            time.write(str(delta.seconds))
    else:
        with open(f"{session}{updating.lower()}.txt","w") as file:
            file.write(message.text)
    subprocess.check_output(f"systemctl restart {session}", shell=True)
    await message.answer(f"{session} uchun {updating.lower()} yangilandi", reply_markup=number_buttons())
    await state.set_state("select_number")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
