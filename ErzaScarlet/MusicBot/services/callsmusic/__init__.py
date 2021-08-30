from pyrogram import Client

from ErzaScarlet import API_HASH, API_ID, SESSION_NAME

client = Client(SESSION_NAME, API_ID, API_HASH)
run = client.run
