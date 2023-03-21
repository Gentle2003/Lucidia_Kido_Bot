import aiogram
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackGame, CallbackQuery, game_high_score


#inline_link = "https://core.telegram.org/bots/inline"
Api_Token = "6279823147:AAHUCmvOtB3d506N2uQrEYyttJ0PMxOo1uA"
bot = Bot(token= Api_Token)
runz = Dispatcher(bot)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

button1 = KeyboardButton("Play")
button2 = KeyboardButton("Restart Bot")
button3 = KeyboardButton("🎮 Lucidia Kido 2")
button4 = KeyboardButton("More Games soon..")
button5 = KeyboardButton("More Games soon..")
button6 = KeyboardButton("More Games soon..")
button7 = KeyboardButton("Cancel")
button8 = InlineKeyboardButton(text = "Play", callback_data= "Lucidiakido", url= "https://telegram-game-mu.vercel.app/")


Keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True).add(button1).add(button2)
Keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True).add(button3, button4).add(button5, button6).add(button7)
keyboard3 = InlineKeyboardMarkup().add(button8)

@runz.message_handler(commands=["start", "help"])
async def welcome_handler(message : types.message):
    bot1 = bot.get_current()
    user = types.User.get_current()
    logger.info("User %s started the conversation.", user.first_name)
    await message.reply(f"Hey {user.first_name}, Welcome🤗 to Lucidia Games Bot providing you the best of games for your entertainment. Join Us💖.", reply_markup= Keyboard)

@runz.message_handler()
async def play_handler(message : types.message):
    if message.text == "Play":
        await message.answer(f"Oooh! I see you can't wait huh?😉  \nPick your game from the menu below let's roll..👇", reply_markup= Keyboard2)

    elif message.text == "Restart Bot":
        await message.answer(f"/start")

    elif message.text == "🎮 Lucidia Kido 2":
        await message.reply("Select: ", reply_markup= keyboard3)
    elif message.text == "More Games soon..":
        await message.answer(f"More games to be hosted soon, stay tuned! :D")

    elif message.text == "Cancel":
        await message.answer(f"Wooh🔥, you still wanna play?", reply_markup = Keyboard)

# @runz.callback_query_handler(text = ["Lucidiakido"])
# async def run_game(call: CallbackQuery):
#     if call.data == "LucidiaKido":
#         await call.answer()

@runz.callback_query_handler(lambda c: c.game_short_name is not None)
async def game_callback_handler(callback_query: CallbackQuery):
    # Get the game_short_name from the callback query
    game_short_name = callback_query.game_short_name
    username = "Lucidia_games_bot"
    print("ckicked button")
    # Build the url to the game page
#    game_url = f'https://t.me/{bot.username}?game={game_short_name}'
    game_url = f'https://t.me/{username}?game={game_short_name}'
    # Answer the callback query with the game page url
    await bot.answer_callback_query(callback_query.id, url="https://telegram-game-mu.vercel.app/")
    print("done this")


# Handler for when a user finishes playing the game
@runz.callback_query_handler(lambda c: c.game_short_name == 'Lucidiakido' and c.data == 'finished')
async def game_finished_handler(callback_query: CallbackQuery):
    # Get the user ID and score
    YOUR_BACKEND_API_ENDPOINT = "https://telegram-game-mu.vercel.app/"
    user_id = callback_query.from_user.id
    score = 0

    # Make a request to your backend to update the user's score
    # and retrieve the updated score
    updated_score = YOUR_BACKEND_API_ENDPOINT(user_id, score)
    print("Updated score")
    # Call the setGameScore method to update the user's score
    await bot.set_game_score(user_id, score=updated_score, chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)

#game_data = "https://telegram-game-mu.vercel.app/"

executor.start_polling(runz)

