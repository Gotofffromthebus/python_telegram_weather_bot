import requests
import datetime
from config import telegram_api_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=telegram_api_token)
dp_ = Dispatcher(bot)


@dp_.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет, напиши название города и я пришлю сводку погоды")

@dp_.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f" http://api.openweathermap.org/data/2.5/weather?q={message.text}&APPID={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = (data['main']['pressure']) // 1.33
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset =  datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(f"*** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n"
              f"Погода в городе: {city} {weather} C°\n"
              f"Влажность воздуха: {humidity} %\n"
              f"Ветер {wind} м/с, Давление: {pressure} мм.рт.ст.\n"
              f"Восход солнца: {sunrise}\n"
              f"Закат солнца: {sunset}\n"
              f"Продолжительность светового дня {length_of_the_day}\n"
              f"Хорошего дня!")

    except:
        await message.reply('Проверь название города!')



if __name__ == '__main__':
    executor.start_polling(dp_)
