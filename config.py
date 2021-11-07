import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Erza Scarlet")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "Sohail")
ALIVE_NAME = getenv("ALIVE_NAME", "Erza")
BOT_USERNAME = getenv("BOT_USERNAME", "ErzaScarlet_GroupBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "ErzaMusic")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "ErzaScarlet_Support")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "ErzaScarlet_Justice")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/c83b000f004f01897fe18.png")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/390d1211ee23949cf0921.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/10e635e84720794ed305f.jpg")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/d913cd536b241f83bbca3.jpg")
