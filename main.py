import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keys import TOKEN, API_KEY




openai.api_key = API_KEY
print(openai.api_key)
bot = Bot(TOKEN)
dp = Dispatcher(bot)

#print(openai.Model.list())

@dp.message_handler(commands= ['start','help'])
async def welcome_message(message: types.Message):
    await message.answer("Hi, you can use ChatGPT via Telegram now!Send me a message.")


@dp.message_handler()
async def chat(message: types.Message):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= message.text,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
    
    await message.answer(response["choices"][0]["text"])
    print(message.text)
    print(response["choices"][0]["text"])




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


