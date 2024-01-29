# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext

from aiogram.utils import executor
import random
import json
from aiogram.dispatcher.filters import Text

from bot import keyboards
from bot.keyboards.buttons import create_keyboard_name_list
from bot.states import UpdateList

with open("tokens.json", "r") as read_file:
    tokens = json.load(read_file)
token = tokens["tokenTG"]

bot = Bot(token)
names_list = ["Екатерина К", "Санечик", "Наташа", "Оксана", "Татьяна", "Настя", "Лера", "Иван",
              "Соня", "Ирен", "Рифат", "Сережа", "Влад", "Юля", "Аня", "Катя Р",
              "Натали Хуторская", "Кирилл"]
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


def get_random_wish():
    wishes = [
        "Пусть ваш день будет наполнен улыбками и радостью!",
        "Желаю вам насыщенного и позитивного дня!",
        "Пусть каждый момент вашего дня приносит вам удовольствие.",
        "Пусть этот день подарит вам море вдохновения и новых возможностей.",
        "Пусть солнце светит ярко в вашем сердце весь день!",
        "Пусть каждый шаг приводит вас к успеху и удовлетворению.",
        "Не забывайте улыбаться, ведь это делает день ярче!",
        "Пусть день будет так же замечательным, как вы!",
        "Желаю вам незабываемых моментов счастья сегодня!",
        "Пусть каждая минута дня принесет вам радость и умиротворение.",
        "Пусть каждая тучка, которую вы увидите, скрывает в себе маленькое счастье.",
        "Пожелание на сегодня: пусть ваш кофе будет горячим, а пробки на дороге — отсутствовать!",
        "Желаю вам, чтобы весь день вас сопровождали забавные случайности и удивительные совпадения.",
        "Пусть ваш день будет настолько ярким, что радуга позавидует!",
        "Желаю вам сегодня ощутить волшебство в самых обыденных вещах.",
        "Пусть каждое препятствие станет для вас ступенькой к новым вершинам.",
        "Желаю вам найти клад в море повседневности и радоваться каждому его открытию.",
        "Пусть этот день пройдет так, словно вы герой вашей любимой книги или фильма.",
        "Желаю вам сегодняшний день воспринимать как чистый холст, готовый принять вашу яркую палитру.",
        "Пусть день будет настолько интересным, что вы найдете ответы на вопросы, о которых даже не задумывались."
    ]

    return random.choice(wishes)


def get_random_smiley():
    smileys = ["😊", "🥰", "🙂", "😋", "😇", "🤩", "😉", "❤️", "💕", "💖", "💗", "💘", "💙", "💚", "💛", "💜"]

    return random.choice(smileys)


async def on_startup(_):
    print('Bot online')
    await bot.send_message("1454049968", "Бот запущен и готов к работе")


@dp.message_handler(commands=['start'])
async def commands_start(message: types.message):
    await bot.send_message(
        message.chat.id,
        "Привет,выбери нужную команду",
        reply_markup=keyboards.main_menu,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(commands=['menu'])
async def commands_menu(message: types.message):
    await bot.send_message(
        message.chat.id,
        "Ты в меню,выбери нужную команду",
        reply_markup=keyboards.main_menu,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(Text(equals=["Исправить список"], ignore_case=True))
async def update_list(message: types.message):
    await UpdateList.start.set()
    await bot.send_message(
        message.chat.id,
        "Выбери из списка имя для удаления",
        reply_markup=create_keyboard_name_list(names_list),
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(Text(equals=["Получить список"], ignore_case=True))
async def update_list(message: types.message):
    sp = list.copy(names_list)
    sp_random = [sp.pop(random.randrange(len(sp))) for _ in range(len(sp))]
    await bot.send_message(message.chat.id, f" {get_random_smiley()} \n ".join(sp_random))
    await bot.send_message(message.chat.id, get_random_wish(), reply_markup=keyboards.main_menu, )
    await bot.send_message(message.chat.id, get_random_smiley())


@dp.message_handler(state=UpdateList.start)
async def start_update_list(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        result = data

    if "names_list" in result:
        update_list = result["names_list"].copy()
        try:
            update_list.remove(message.text)
        except ValueError as error:
            print(error)
        async with state.proxy() as data:
            data["names_list"] = update_list
        await UpdateList.update.set()
        await bot.send_message(
            message.chat.id,
            "Выбери следующую команду",
            reply_markup=keyboards.step_keyboard,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    else:
        new_name_list = names_list.copy()
        try:
            new_name_list.remove(message.text)
        except ValueError as error:
            print(error)
        async with state.proxy() as data:
            data["names_list"] = new_name_list
        await UpdateList.update.set()
        await bot.send_message(
            message.chat.id,
            "Выбери следующую команду",
            reply_markup=keyboards.step_keyboard,
            parse_mode=types.ParseMode.MARKDOWN,
        )


@dp.message_handler(state=UpdateList.update)
async def start_update_list(message: types.Message, state: FSMContext):
    if message.text in names_list:
        async with state.proxy() as data:
            result = data
        if "names_list" in result:
            update_list = result["names_list"].copy()
            try:
                update_list.remove(message.text)
            except ValueError as error:
                print(error)
            async with state.proxy() as data:
                data["names_list"] = update_list
        else:
            new_name_list = names_list
            try:
                new_name_list.remove(message.text)
            except ValueError as error:
                print(error)
            async with state.proxy() as data:
                data["names_list"] = new_name_list
        async with state.proxy() as data:
            res = data["names_list"]
        await bot.send_message(
            message.chat.id,
            "Выбери следующее действие",
            reply_markup=keyboards.step_keyboard,
            parse_mode=types.ParseMode.MARKDOWN, )
        async with state.proxy() as data:
            res = data["names_list"]
        await UpdateList.update.set()
    elif message.text == "Удалить ещё":
        async with state.proxy() as data:
            res = data["names_list"]
        await bot.send_message(
            message.chat.id,
            "Выбери из списка имя для удаления",
            reply_markup=create_keyboard_name_list(res),
            parse_mode=types.ParseMode.MARKDOWN,
        )
        await UpdateList.update.set()
    elif message.text == "Закончить":
        async with state.proxy() as data:
            res = data["names_list"]
        sp = list.copy(res)
        sp_random = [sp.pop(random.randrange(len(sp))) for _ in range(len(sp))]
        await bot.send_message(message.chat.id, f" {get_random_smiley()} \n ".join(sp_random))
        await bot.send_message(message.chat.id, get_random_wish(), reply_markup=keyboards.main_menu, )
        await bot.send_message(message.chat.id, get_random_smiley())

        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
