import telebot.types
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from threading import Thread
from telebot.apihelper import ApiTelegramException
import logging

Api_Token = "6279823147:AAHUCmvOtB3d506N2uQrEYyttJ0PMxOo1uA"
bot = TeleBot(Api_Token)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


button1 = KeyboardButton("Play")
button2 = KeyboardButton("Restart Bot")
button3 = KeyboardButton("🎮 Lucidia Karate 2")
button4 = KeyboardButton("More Games soon..")
button5 = KeyboardButton("More Games soon..")
button6 = KeyboardButton("More Games soon..")
button7 = KeyboardButton("Cancel")


Keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True).add(button1).add(button2)
Keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True).add(button3, button4).add(button5, button6).add(button7)

@bot.message_handler(commands=["start", "help"])
def welcome_handler(message:Message):
    user = message.chat.username
    user1 = telebot.types.User
    logger.info("User %s started the conversation.", user)
    bot.reply_to(message, f"Hey {user}, Welcome🤗 to Lucidia Games Bot providing you the best of games for your entertainment. Join Us💖.", reply_markup= Keyboard)

@bot.message_handler()
def play_handler(message):
    if message.text == "Play":
        bot.reply_to(message, f"Oooh! I see you can't wait huh?😉  \nPick your game from the menu below let's roll..👇", reply_markup=Keyboard2)

    elif message.text == "Restart Bot":
        bot.reply_to(message, f"/start")

    elif message.text == "🎮 Lucidia Karate 2":

        buttonplay = InlineKeyboardButton(text = "Play alone", callback_game= "Lucidiakido")
        buttonshare = InlineKeyboardButton(text= "Share", url= "http://t.me/Lucidia_games_bot?game=Lucidiakido")
        main_keyboard = InlineKeyboardMarkup().add(buttonplay,buttonshare)
        bot.send_game(chat_id= message.chat.id,game_short_name="LucidiaKido", reply_markup= main_keyboard)

    elif message.text == "More Games soon..":
        bot.send_message(message.chat.id, f"More games to be hosted soon, stay tuned! :D")

    elif message.text == "Cancel":
        bot.send_message(message.chat.id, f"Wooh🔥, you still wanna play?", reply_markup = Keyboard)

@bot.callback_query_handler(lambda c: c.game_short_name is not None)
def game_callback_handler(callback_query:CallbackQuery):
    bot.answer_callback_query(callback_query.id, url=f"https://telegram-game-mu.vercel.app?user_id={callback_query.from_user.id}&msg_id={callback_query.inline_message_id}")

def run():
    import json, time
    def load_file(file_name="data.json"):
        with open(file_name) as json_file:
            data = json.load(json_file)
            return data

    def write_in_file(data, file_name="data.json"):
        with open(file_name, "w") as f:
            json.dump(data, f)

    while True:
        time.sleep(2)
        data = load_file()
        if len(data) > 0:
            for user in data:
                # Remove anything that has been there longer than 5 seconds
                if time.time() - user["time"] > 5:
                    data.remove(user)
                    write_in_file(data)
                    continue
                try:
                    bot.set_game_score(int(user["user_id"]), int(user["score"]), inline_message_id=user["msg_id"])
                except ApiTelegramException:
                    continue

Thread(target=run, daemon=True).start()
bot.infinity_polling()
