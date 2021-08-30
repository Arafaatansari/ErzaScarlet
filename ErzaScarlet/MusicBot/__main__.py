import requests
from pyrogram import Client as Bot

from ErzaScarlet import API_HASH
from ErzaScarlet import API_ID
from ErzaScarlet import BG_IMAGE
from ErzaScarlet import TOKEN
from ErzaScarlet.MusicBot.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="DaisyXMusic.modules"),
)

bot.start()
run()