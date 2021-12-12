import io
import sys
import traceback
import os
import re
import subprocess
import asyncio
import requests
import tracemoepy
from bson.objectid import ObjectId
from bs4 import BeautifulSoup as bs
from datetime import datetime
from natsort import natsorted
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ChannelInvalid as ci, ChannelPrivate as cp, PeerIdInvalid as pi, FloodWait as fw
from ErzaScarlet import BOT_USERNAME as BOT_NAME, TRIGGERS as trg, DEV_USERS as OWNER, pbot as anibot, DOWN_PATH, EVENT_LOGS as LOG_CHANNEL_ID
from ErzaScarlet.helper_extra.db import get_collection
from ErzaScarlet.helper_extra.helper import (
    AUTH_USERS, clog, check_user, control_user, rand_key, return_json_senpai,
    runcmd, take_screen_shot, IGNORE, media_to_image, make_it_rw,
    USER_JSON, USER_WC
)
from ErzaScarlet.helper_extra.data_parser import (
    get_all_genres, get_all_tags, get_top_animes, get_user_activity, get_user_favourites, toggle_favourites, parse_filler,
    get_anime, get_airing, get_anilist, get_character, get_additional_info, get_manga, browse_, get_wo, get_wols, AIR_QUERY,
    get_featured_in_lists, update_anilist, get_user, ANIME_DB, MANGA_DB, CHAR_DB, get_scheduled, search_filler, ANIME_QUERY,
    ACTIVITY_QUERY, ALLTOP_QUERY, ANILIST_MUTATION, ANILIST_MUTATION_DEL, ANILIST_MUTATION_UP, ANIME_MUTATION, BROWSE_QUERY,
    ANIME_TEMPLATE, CHA_INFO_QUERY, CHAR_MUTATION, CHARACTER_QUERY, DES_INFO_QUERY, DESC_INFO_QUERY, FAV_ANI_QUERY, GET_TAGS,
    FAV_CHAR_QUERY, FAV_MANGA_QUERY, GET_GENRES, ISADULT, LS_INFO_QUERY, MANGA_MUTATION, MANGA_QUERY, PAGE_QUERY, TOP_QUERY,
    REL_INFO_QUERY, TOPT_QUERY, USER_QRY, VIEWER_QRY
)
from .anibotanilist import auth_link_cmd, code_cmd, logout_cmd

USERS = get_collection("USERS")
GROUPS = get_collection("GROUPS")
SFW_GROUPS = get_collection("SFW_GROUPS")
DC = get_collection('DISABLED_CMDS')
AG = get_collection('AIRING_GROUPS')
CR_GRPS = get_collection('CRUNCHY_GROUPS')
HD_GRPS = get_collection('HEADLINES_GROUPS')
SP_GRPS = get_collection('SUBSPLEASE_GROUPS')
CMD = [
    'anime',
    'anilist',
    'character',
    'manga',
    'airing',
    'help',
    'schedule',
    'fillers',
    'top',
    'reverse',
    'watch',
    'start',
    'ping',
    'flex',
    'me',
    'activity',
    'user',
    'favourites',
    'gettags',
    'quote',
    'getgenres'
]


@anibot.on_message(~filters.private & filters.command(['anidisable', f'anidisable{BOT_NAME}', 'anienable', f'anienable{BOT_NAME}']))
@control_user
async def en_dis__able_cmd(client: anibot, message: Message, mdata: dict):
    cmd = mdata['text'].split(" ", 1)
    gid = mdata['chat']['id']
    user = mdata['from_user']['id']
    if user in OWNER or (await anibot.get_chat_member(gid, user)).status!='member':
        if len(cmd)==1:
            x = await message.reply_text('No command specified to be disabled!!!')
            await asyncio.sleep(5)
            await x.delete()
            return
        enable = False if not 'enable' in cmd[0] else True
        if set(cmd[1].split()).issubset(CMD):
            find_gc = await DC.find_one({'_id': gid})
            if find_gc is None:
                if enable:
                    x = await message.reply_text('Command already enabled!!!')
                    await asyncio.sleep(5)
                    await x.delete()
                    return
                await DC.insert_one({'_id': gid, 'cmd_list': cmd[1]})
                x = await message.reply_text("Command disabled!!!")
                await asyncio.sleep(5)
                await x.delete()
                return
            else:
                ocls: str = find_gc['cmd_list']
                if set(cmd[1].split()).issubset(ocls.split()):
                    if enable:
                        if len(ocls.split())==1:
                            await DC.delete_one({'_id': gid})
                            x = await message.reply_text("Command enabled!!!")
                            await asyncio.sleep(5)
                            await x.delete()
                            return
                        ncls = ocls.split()
                        for i in cmd[1].split():
                            ncls.remove(i)
                        ncls = " ".join(ncls)
                    else:
                        x = await message.reply_text('Command already disabled!!!')
                        await asyncio.sleep(5)
                        await x.delete()
                        return
                else:
                    if enable:
                        x = await message.reply_text('Command already enabled!!!')
                        await asyncio.sleep(5)
                        await x.delete()
                        return
                    else:
                        lsncls = []
                        prencls = (ocls+' '+cmd[1]).replace('  ', ' ')
                        for i in prencls.split():
                            if i not in lsncls:
                                lsncls.append(i)
                        ncls = " ".join(lsncls)
                await DC.update_one({'_id': gid}, {'$set': {'cmd_list': ncls}})
                x = await message.reply_text(f"Command {'dis' if enable is False else 'en'}abled!!!")
                await asyncio.sleep(5)
                await x.delete()
                return
        else:
            await message.reply_text("Hee, is that a command?!")


@anibot.on_message(~filters.private & filters.command(['disabled', f'disabled{BOT_NAME}']))
@control_user
async def list_disabled(client: anibot, message: Message, mdata: dict):
    find_gc = await DC.find_one({'_id': mdata['chat']['id']})
    if find_gc is None:
        await message.reply_text("No commands disabled in this group!!!")
    else:
        lscmd = find_gc['cmd_list'].replace(" ", "\n")
        await message.reply_text(f"List of commands disabled in **{mdata['chat']['title']}**\n\n{lscmd}")


@anibot.on_message(filters.user(OWNER) & filters.command(['dbcleanup', f'dbcleanup{BOT_NAME}'], prefixes=trg))
@control_user
async def db_cleanup(client: anibot, message: Message, mdata: dict):
    count = 0
    entries = ""
    st = datetime.now()
    x = await message.reply_text("Starting database cleanup in 5 seconds")
    et = datetime.now()
    pt = (et-st).microseconds / 1000
    await asyncio.sleep(5)
    await x.edit_text("Checking 1st collection!!!")
    async for i in GROUPS.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['id'])
        except cp:
            count += 1
            entries += str(await GROUPS.find_one({'id': i['id']}))+'\n\n'
            await GROUPS.find_one_and_delete({'id': i['id']})
        except ci:
            count += 1
            entries += str(await GROUPS.find_one({'id': i['id']}))+'\n\n'
            await GROUPS.find_one_and_delete({'id': i['id']})
        except pi:
            count += 1
            entries += str(await GROUPS.find_one({'id': i['id']}))+'\n\n'
            await GROUPS.find_one_and_delete({'id': i['id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 2nd collection!!!")
    async for i in SFW_GROUPS.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['id'])
        except cp:
            count += 1
            entries += str(await SFW_GROUPS.find_one({'id': i['id']}))+'\n\n'
            await SFW_GROUPS.find_one_and_delete({'id': i['id']})
        except ci:
            count += 1
            entries += str(await SFW_GROUPS.find_one({'id': i['id']}))+'\n\n'
            await SFW_GROUPS.find_one_and_delete({'id': i['id']})
        except pi:
            count += 1
            entries += str(await SFW_GROUPS.find_one({'id': i['id']}))+'\n\n'
            await SFW_GROUPS.find_one_and_delete({'id': i['id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 3rd collection!!!")
    async for i in DC.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['_id'])
        except cp:
            count += 1
            entries += str(await DC.find_one({'_id': i['_id']}))+'\n\n'
            await DC.find_one_and_delete({'_id': i['_id']})
        except ci:
            count += 1
            entries += str(await DC.find_one({'_id': i['_id']}))+'\n\n'
            await DC.find_one_and_delete({'_id': i['_id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 4th collection!!!")
    async for i in AG.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['_id'])
        except cp:
            count += 1
            entries += str(await AG.find_one({'id': i['_id']}))+'\n\n'
            await AG.find_one_and_delete({'_id': i['_id']})
        except ci:
            count += 1
            entries += str(await AG.find_one({'id': i['_id']}))+'\n\n'
            await AG.find_one_and_delete({'_id': i['_id']})
        except pi:
            count += 1
            entries += str(await AG.find_one({'id': i['_id']}))+'\n\n'
            await AG.find_one_and_delete({'_id': i['_id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 5th collection!!!")
    async for i in AUTH_USERS.find():
        if i['id']=='pending':
            count += 1
            entries += str(await AUTH_USERS.find_one({'_id': i['_id']}))+'\n\n'
            await AUTH_USERS.find_one_and_delete({'_id': i['_id']})
    async for i in AUTH_USERS.find():
        await asyncio.sleep(2)
        try:
            await client.get_users(i['id'])
        except pi:
            count += 1
            entries += str(await AUTH_USERS.find_one({'id': i['id']}))+'\n\n'
            await AUTH_USERS.find_one_and_delete({'id': i['id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 6th collection!!!")
    async for i in CR_GRPS.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['_id'])
        except cp:
            count += 1
            entries += str(await CR_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await CR_GRPS.find_one_and_delete({'_id': i['_id']})
        except ci:
            count += 1
            entries += str(await CR_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await CR_GRPS.find_one_and_delete({'_id': i['_id']})
        except pi:
            count += 1
            entries += str(await CR_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await CR_GRPS.find_one_and_delete({'_id': i['_id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 7th collection!!!")
    async for i in SP_GRPS.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['_id'])
        except cp:
            count += 1
            entries += str(await SP_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await SP_GRPS.find_one_and_delete({'_id': i['_id']})
        except ci:
            count += 1
            entries += str(await SP_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await SP_GRPS.find_one_and_delete({'_id': i['_id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)
    await x.edit_text("Checking 8th collection!!!")
    async for i in HD_GRPS.find():
        await asyncio.sleep(2)
        try:
            await client.get_chat(i['_id'])
        except cp:
            count += 1
            entries += str(await HD_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await HD_GRPS.find_one_and_delete({'_id': i['_id']})
        except ci:
            count += 1
            entries += str(await HD_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await HD_GRPS.find_one_and_delete({'_id': i['_id']})
        except pi:
            count += 1
            entries += str(await HD_GRPS.find_one({'_id': i['_id']}))+'\n\n'
            await HD_GRPS.find_one_and_delete({'_id': i['_id']})
        except fw:
            await asyncio.sleep(fw.x + 5)
    await asyncio.sleep(5)

    nosgrps = await GROUPS.estimated_document_count()
    nossgrps = await SFW_GROUPS.estimated_document_count()
    nosauus = await AUTH_USERS.estimated_document_count()
    if count == 0:
        msg = f"""Database seems to be accurate, no changes to be made!!!
**Groups:** `{nosgrps}`
**SFW Groups:** `{nossgrps}`
**Authorised Users:** `{nosauus}`
**Ping:** `{pt}`
"""
    else:
        msg = f"""{count} entries removed from database!!!
**New Data:**
    __Groups:__ `{nosgrps}`
    __SFW Groups:__ `{nossgrps}`
    __Authorised Users:__ `{nosauus}`
**Ping:** `{pt}`
"""
        if len(entries)>4095:
            with open('entries.txt', "w+") as file:
                file.write(entries)
            return await x.reply_document('entries.txt')
        await x.reply_text(entries)
    await x.edit_text(msg)


@anibot.on_message(filters.user(OWNER) & filters.command(['anibotstats', f'anibotstats{BOT_NAME}'], prefixes=trg))
@control_user
async def stats_(client: anibot, message: Message, mdata: dict):
    st = datetime.now()
    x = await message.reply_text("Collecting Stats!!!")
    et = datetime.now()
    pt = (et-st).microseconds / 1000
    nosus = await USERS.estimated_document_count()
    nosauus = await AUTH_USERS.estimated_document_count()
    nosgrps = await GROUPS.estimated_document_count()
    nossgrps = await SFW_GROUPS.estimated_document_count()
    noshdgrps = await HD_GRPS.estimated_document_count()
    s = await SP_GRPS.estimated_document_count()
    a = await AG.estimated_document_count()
    c = await CR_GRPS.estimated_document_count()
    kk = requests.get("https://api.github.com/repos/lostb053/anibot").json()
    await x.edit_text(f"""
Stats:-
**Users:** {nosus}
**Authorised Users:** {nosauus}
**Groups:** {nosgrps}
**Airing Groups:** {a}
**Crunchyroll Groups:** {c}
**Subsplease Groups:** {s}
**Headline Groups:** {noshdgrps}
**SFW Groups:** {nossgrps}
**Stargazers:** {kk.get("stargazers_count")}
**Forks:** {kk.get("forks")}
**Ping:** `{pt} ms`
"""
    )


@anibot.on_message(filters.private & filters.command(['feedback', f'feedback{BOT_NAME}'], prefixes=trg))
@control_user
async def feed_(client: anibot, message: Message, mdata: dict):
    owner = (await client.get_users(OWNER[0])).username
    await client.send_message(mdata['chat']['id'], f"For issues or queries please contact @{owner} or join @hanabi_support")



##########################################################################