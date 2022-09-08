from bs4 import BeautifulSoup
import requests
import logging
from tqdm import tqdm
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

API_TOKEN = '2077928296:AAF8eOqCbM6wiESf-HxO6OOOJPaYrQ4rZ1s'
logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):

    await message.answer(message.text)

    # with open('iPhone11.txt', 'w') as file:
    #     request = 'https://www.olx.uz/d/elektronika/telefony/mobilnye-telefony/samarkand/q-iPhone-XS-max-256/?currency=UZS&search%5Border%5D=filter_float_price:asc'
    #
    #     r = requests.get(request, params={'page': 1})
    #     page = BeautifulSoup(r.content, 'html.parser')
    #     headers = page.select('div.css-19ucd76')
    #
    #     test_headers = [headers[0], headers[1], headers[2]]
    #
    #     for i in tqdm(headers):
    #         if "ТОП" not in i.text:
    #             if i.select('h6.eu5v0x0') != []:
    #                 link = 'https://www.olx.uz' + str(i.select('a.css-1bbgabe')[0]['href'])
    #                 request_item = requests.get(link)
    #                 item_page = BeautifulSoup(request_item.content, 'html.parser')
    #                 title = i.select('h6.eu5v0x0')[0].text
    #                 text = item_page.select('div.css-g5mtbi-Text')[0].text
    #                 price = item_page.select('h3.css-okktvh-Text')[0].text
    #                 img = item_page.select('img.css-1bmvjcs')
    #                 if img != []:
    #                     img_for_send = img[0]['src']
    #                 else:
    #                     img_for_send = False
    #                 file.write(title + '\n')
    #                 file.write(price + '\n')
    #                 file.write(text + '\n')
    #                 file.write(link + '\n')
    #                 file.write('\n\n\n\n')
    #                 inline_link = KeyboardButton('Перейти на сайт', url=link)
    #                 inline_kb = InlineKeyboardMarkup().add(inline_link)
    #                 message_text = title + '\n\n' + '💰' + price + '\n\n' + text
    #                 if img_for_send:
    #                     await bot.send_photo(message.chat.id, img_for_send, caption=message_text, reply_markup=inline_kb)
    #                 else:
    #                     await bot.send_message(message.chat.id, message_text, reply_markup=inline_kb)
    #
    # print('Done!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
