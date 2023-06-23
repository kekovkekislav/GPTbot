import openai   


from aiogram import Bot, types,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from keys import TOKEN, API_KEY, weather_key
import requests
from pprint import pprint
from datetime import date, time, datetime
import math
from generate import generate_response




openai.api_key = API_KEY
print(openai.api_key)
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage= MemoryStorage())


#print(openai.Model.list())


class GPTMode(StatesGroup):
    GPT = State()

@dp.message_handler(commands= ['start','help'])
async def welcome_message(message: types.Message):
    await message.answer("Hi, you can use ChatGPT via Telegram now!Send me a message.")


##START GPT STATE
@dp.message_handler(commands = ["gpt"])
async def gpt_enable(message: types.Message):
    await message.answer("You'r enabled chatGPT mode. Your next message will start a conversation!")
    await GPTMode.GPT.set()

##CLOSE GPT STATE
@dp.message_handler(Text(equals="/stopgpt", ignore_case=True), state="*")
@dp.message_handler(Command("stopgpt"), state="*")
async def gpt_disable(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("You'r disabled chatGPT mode.")

##WEATHER COMMAND
@dp.message_handler(Command("weather"))
async def weather_command(message: types.Message):
    await message.answer("Напиши мне название города и я пришлю тебе погоду в нём!")

## WEATHER CITY HANDLER
@dp.message_handler()
async def send_weather(message: types.Message):
        try:
            r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={message.text}&aqi=no&lang=ru")
            data = r.json()
            country = data["location"]["country"]
            city = data["location"]["name"]
            cur_weather = math.floor(data["current"]["temp_c"])
            weather_description = data["current"]["condition"]["text"]
            weather_feelslike = math.floor(data["current"]["feelslike_c"])
            wind = math.floor(int(data["current"]["wind_kph"]) // 3.6)
            humidity = data["current"]["humidity"]

            await message.answer(
    f"\U0001F551{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    f"_Местоположение_: *{country}*, *{city}*\n"
    f"\U0001F321_Температура_: *{cur_weather}°C*, *{weather_description}*\n"
    f"🧍‍♂️_По ощущениям_: *{weather_feelslike}°C*\n"
    f"\U0001F32A_Ветер_: *{wind}m/s*\n"
    f"\U0001F4A7_Влажность:_ *{humidity}%*\n"
    f"\n*Хорошего дня!*",
    parse_mode=types.ParseMode.MARKDOWN
)
    

        except:
            await message.answer("Ошибка! Проверьте название города!")
   

##GPT RESPONSE 
@dp.message_handler(state = GPTMode.GPT)
async def chat(message: types.Message, state: FSMContext):
    gpt_response = generate_response(prompt=message.text)
    await message.answer(gpt_response["choices"][0]["text"])
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



