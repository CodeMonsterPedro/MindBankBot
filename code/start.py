import config
from aiogram import Bot, Dispatcher, executor, types
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    if message.from_user.id not in config.MAIN_USER_ID:
        await message.answer('How are u? -_-')
    inputStr = message.text
    await message.answer(str(inputStr))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)    
