import requests
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from bs4 import BeautifulSoup

from config import API_TOKEN
from kb import main_kb, cities_kb


logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Request(StatesGroup):
    main_menu = State()
    request = State()
    region = State()
    show_results = State()


def show_quantity(request, region='list'):
    url = 'https://www.olx.uz/d/{1}/q-{0}/'.format(request, region)
    r = requests.get(url, params={'page': 1})
    page = BeautifulSoup(r.content, 'html.parser')
    if page.select('div[data-testid=total-count]'):
        results = page.select('div[data-testid=total-count]')[0].text
        results = results.split(' ')
        if results[3] == '1\xa0000':
            answer_text = 'Найдено результатов: более {0}'.format(results[3])
        else:
            answer_text = 'Найдено результатов: {0}'.format(results[3])
    else:
        answer_text = 'Результаты не найдены'
    return answer_text


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await Request.main_menu.set()
    await message.reply("Добро пожаловать в бот, используйте меню", reply_markup=main_kb())


@dp.message_handler()
async def echo(message: types.Message):
    await Request.main_menu.set()
    await message.answer("Главное меню", reply_markup=main_kb())


@dp.message_handler(state=Request.main_menu)
async def main_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '🔎 Поиск':
            await Request.request.set()
            await message.answer('Укажите запрос')
        elif message.text == '🌎 Выбрать регион':
            await Request.region.set()
            await message.answer('Укажите регион', reply_markup=cities_kb())
        elif message.text == '🗒 Показать результаты':
            if 'request' in data:
                await message.answer('Идет подготовка результатов, пожалуйста подождите')
                if 'region' in data:
                    url = 'https://www.olx.uz/d/{1}/q-{0}/'.format(data['request'], data['region'])
                else:
                    url = 'https://www.olx.uz/d/list/q-{0}/'.format(data['request'])
                r = requests.get(url, params={'page': 1})
                page = BeautifulSoup(r.content, 'html.parser')
                headers = page.select('div.css-19ucd76')
                posts = []
                for i in headers:
                    if "ТОП" not in i.text:
                        if i.select('h6.eu5v0x0'):
                            link = 'https://www.olx.uz' + str(i.select('a.css-1bbgabe')[0]['href'])
                            request_item = requests.get(link)
                            item_page = BeautifulSoup(request_item.content, 'html.parser')
                            title = i.select('h6.eu5v0x0')[0].text
                            text = item_page.select('div.css-g5mtbi-Text')[0].text
                            price = item_page.select('h3.css-okktvh-Text')[0].text
                            img = item_page.select('img.css-1bmvjcs')
                            if img:
                                img_for_send = img[0]['src']
                            else:
                                img_for_send = False
                            item = {
                                'title': title,
                                'text': text,
                                'img': img_for_send,
                                'price': price,
                                'link': link
                            }
                            if item not in posts:
                                posts.append(item)
                divided_posts = []
                collected_divided_posts = []
                for item in posts:
                    if len(divided_posts) < 10:
                        divided_posts.append(item)
                    else:
                        collected_divided_posts.append(divided_posts)
                        divided_posts = [item]
                if collected_divided_posts:
                    if collected_divided_posts[-1] != divided_posts:
                        collected_divided_posts.append(divided_posts)
                else:
                    collected_divided_posts.append(divided_posts)
                data['posts'] = collected_divided_posts
                n = 1
                pages_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                for _ in collected_divided_posts:
                    first_part = 1 + (10 * (n - 1))
                    second_part = n * 10
                    pages_kb.add(KeyboardButton('{0} - {1}'.format(first_part, second_part)))
                    n += 1
                pages_kb.add(KeyboardButton('Назад в меню'))
                await Request.show_results.set()
                await message.answer('Всего подготовлено {0} объявлений'.format(len(posts)), reply_markup=pages_kb)
            else:
                await message.answer('Пожалуйста, сначала укажите запрос в поиске', reply_markup=main_kb())
        elif message.text == '❌ Сброс поиска':
            if 'request' in data:
                del data['request']
            if 'region' in data:
                del data['region']
            await message.answer('Настройки поиска сброшены', reply_markup=main_kb())
        else:
            await message.answer('Пожалуйста, используйте меню', reply_markup=main_kb())


@dp.message_handler(state=Request.request)
async def set_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request'] = message.text.replace(' ', '-')
        await Request.main_menu.set()
        if 'region' in data:
            answer_text = show_quantity(data['request'], data['region'])
        else:
            answer_text = show_quantity(data['request'])
        if answer_text == 'Результаты не найдены':
            del data['request']
        await message.answer(answer_text, reply_markup=main_kb())


@dp.message_handler(state=Request.region)
async def set_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Весь Узбекистан':
            if 'region' in data:
                del data['region']
            answer_text = 'Регион сброшен'
            if 'request' in data:
                answer_text += '\n\n'
                answer_text += show_quantity(data['request'])
            await Request.main_menu.set()
            await message.answer(answer_text, reply_markup=main_kb())
        elif message.text == 'Ташкент':
            data['region'] = 'tashkent'
            answer_text = 'Регион изменен'
            if 'request' in data:
                answer_text += '\n\n'
                answer_text += show_quantity(data['request'], data['region'])
            await Request.main_menu.set()
            await message.answer(answer_text, reply_markup=main_kb())
        elif message.text == 'Самарканд':
            data['region'] = 'samarkand'
            answer_text = 'Регион изменен'
            if 'request' in data:
                answer_text += '\n\n'
                answer_text += show_quantity(data['request'], data['region'])
            await Request.main_menu.set()
            await message.answer(answer_text, reply_markup=main_kb())
        else:
            await message.answer('Пожалуйста укажите правильный город')


@dp.message_handler(state=Request.show_results)
async def show_results(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Назад в меню':
            await Request.main_menu.set()
            await message.answer('Главное меню', reply_markup=main_kb())
        else:
            try:
                pages = data['posts'][int((int(message.text.split(' ')[2]) / 10) - 1)]
            except IndexError:
                pages = False
            except ValueError:
                pages = False
            if pages:
                for item in pages:
                    inline_link = KeyboardButton('Перейти на сайт', url=item['link'])
                    inline_kb = InlineKeyboardMarkup().add(inline_link)
                    if len(item['text']) < 500:
                        message_text = item['title'] + '\n\n' + '💰' + item['price'] + '\n\n' + item['text']
                    else:
                        message_text = item['title'] + '\n\n' + '💰' + item['price']
                    if item['img']:
                        await bot.send_photo(message.chat.id, item['img'], caption=message_text,
                                             reply_markup=inline_kb)
                    else:
                        await bot.send_message(message.chat.id, message_text, reply_markup=inline_kb)
            else:
                await message.answer('Пожалуйста, используйте кнопки для навигации')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
