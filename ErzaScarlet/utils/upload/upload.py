import io
import os
import re
import time
from datetime import datetime
from pathlib import Path

import stagger
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery

from ErzaScarlet import pbot
from ErzaScarlet.utils import Message

async def doc_upload(
    message: Message,
    path,
    del_path: bool = False,
    extra: str = "",
    with_thumb: bool = True,
):
    str_path = str(path)
    sent: Message = await message.client.send_message(
        message.chat.id, f"`Uploading {str_path} as a doc ... {extra}`"
    )
    start_t = datetime.now()
    thumb = None
    if with_thumb:
        thumb = await get_thumb(str_path)
    await message.client.send_chat_action(message.chat.id, "upload_document")
    try:
        msg = await message.client.send_document(
            chat_id=message.chat.id,
            document=str_path,
            thumb=thumb,
            caption=path.name,
            parse_mode="html",
            disable_notification=True,
            progress=progress,
            progress_args=(message, f"uploading {extra}", str_path),
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)

async def photo_upload(message: Message, path, del_path: bool = False, extra: str = ""):
    str_path = str(path)
    sent: Message = await message.client.send_message(
        message.chat.id, f"`Uploading {path.name} as photo ... {extra}`"
    )
    start_t = datetime.now()
    await message.client.send_chat_action(message.chat.id, "upload_photo")
    try:
        msg = await message.client.send_photo(
            chat_id=message.chat.id,
            photo=str_path,
            caption=path.name,
            parse_mode="html",
            disable_notification=True,
            progress=progress,
            progress_args=(message, f"uploading {extra}", str_path),
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)

async def finalize(message: Message, msg: Message, start_t):
    await CHANNEL.fwd_msg(msg)
    await message.client.send_chat_action(message.chat.id, "cancel")
    if message.process_is_canceled:
        await message.edit("`Process Canceled!`", del_in=5)
    else:
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await message.edit(f"Uploaded in {m_s} seconds", del_in=10)                        