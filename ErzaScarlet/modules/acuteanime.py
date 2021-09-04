import requests as r
import telegram

from telegram.ext import (
    MessageHandler,
    CommandHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, ParseMode

from ErzaScarlet import dispatcher, typing
from ErzaScarlet.helper_extra import strings as st
from ErzaScarlet.helper_extra.parsedata import sort_caps
from ErzaScarlet.helper_extra.keyboard import keyboard

base_url = "https://kitsu.io/api/edge"
tempdict = {}



@run_async
@typing
def anime(update, context):
    msg = update.effective_message
    user = update.effective_user
    query = msg.text.replace(" ", "%20")

    res = r.get(f"{base_url}/anime?filter%5Btext%5D={query}")
    if res.status_code != 200:
        msg.reply_text(st.API_ERR)
        return 1

    res = res.json()["data"]
    if len(res) <= 0:
        msg.reply_text(st.NOT_FOUND)
        return 1

    # Add results array with user's id as key
    tempdict[user.id] = res

    keyb = []
    for x in enumerate(res):
        titles = x[1]["attributes"]["titles"]
        keyb.append(
            [
                InlineKeyboardButton(
                    text=f"{titles.get('en') if titles.get('en') else titles.get('ja_jp')}",
                    callback_data=f"anime_{x[0]}_{user.id}",
                )
            ]
        )

    msg.reply_text(
        f"🔍 Search results for {msg.text}:",
        reply_markup=InlineKeyboardMarkup(keyb[:6]),
    )

    return ConversationHandler.END


@run_async
def anime_button(update, context):
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user

    spl = query.data.split("_")
    x, user_id = int(spl[1]), int(spl[2])
    if user.id != user_id:
        return query.answer(st.NOT_ALLOWED, show_alert=True)

    try:
        res = tempdict[user_id]
    except KeyError:
        return query.answer(st.KEYERROR, show_alert=True)

    query.answer("Hold on...")
    query.message.delete()

    data = res[x]["attributes"]
    caption = st.ANIME_STR.format(
        data["titles"].get("en", ""),
        data["titles"].get("ja_jp", ""),
        data.get("subtype", "N/A"),
        data.get("ageRatingGuide", "N/A"),
        data.get("averageRating", "N/A"),
        data.get("status", "N/A"),
        data.get("startDate", "N/A"),
        data.get("endDate", "N/A"),
        data.get("episodeLength", "N/A"),
        data.get("episodeCount", "N/A"),
        data.get("synopsis", "N/A"),
    )

    if data.get("posterImage"):
        context.bot.sendPhoto(
            chat_id=chat.id,
            photo=data["posterImage"]["original"],
            caption=sort_caps(caption, c_id=res[x]["id"], anime=True),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                keyboard(
                    title=data["titles"].get("en"),
                    anime_ytkey=data.get("youtubeVideoId"),
                    anime_id=res[x]["id"],
                )
            ),
            timeout=60,
            disable_web_page_preview=True,
        )

    else:
        context.bot.sendMessage(
            chat.id,
            text=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                keyboard(
                    title=data["titles"].get("en"),
                    anime_ytkey=data.get("youtubeVideoId"),
                    anime_id=res[x]["id"],
                )
            ),
            disable_web_page_preview=True,
        )
    del tempdict[user_id]


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


AN_BUTTON_HANDLER = CallbackQueryHandler(anime_button, pattern=r"anime_")

dispatcher.add_handler(AN_BUTTON_HANDLER)