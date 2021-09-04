#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2020 Stɑrry Shivɑm // This file is part of AcuteBot
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from ErzaScarlet import __version__
from platform import python_version
from telegram import __version__ as _libv_

# Contents
MOVIE_STR = """
️**{}** : {}

• Status : `{}`
• Genres : `{}`
• Languages : `{}`
• Runtime : `{} minutes`
• Budget : `{}`
• Revenue : `{}`
• Release Date : `{}`
• Average Rating : `{}`
• Popularity : `{}`

• OverView : <em>{}</em>
"""

TV_STR = """
**{}**

• Created by : `{}`
• Genres : `{}`
• Languages : `{}`
• Episodes Runtime : `{}`
• First aired : `{}`
• Last aired : `{}`
• Status : `{}`
• Seasons : `{}`
• Total EPs : `{}`
• Average Rating : `{}`
• Production Company : `{}`

• OverView : <em>{}</em>
"""

ANIME_STR = f"""
**{}** | **{}**

• Type : `{}`
• Category : `{}`
• Average Rating : `{}`
• Status : `{}`
• First aired : `{}`
• Last aired : `{}`
• Runtime : `{} minutes`
• No of episodes : `{}`

• Synopsis : <em>{}</em>
"""

MANGA_STR = """
**{}** | **{}**
• Type : `{}`
• Average Rating : `{}`
• Status : `{}`
• First release : `{}`
• Last release : `{}`
• Volume count : `{}`
• No of chapters : `{}`
• Serialization : `{}`

• Synopsis : <em>{}</em>
"""

# Inline Content
INLINE_STR = """
• **Title** : {}
• **Release** : `{}`
• **Popularity** : `{}`
• **Language** : `{}`
• **Average Rating** : `{}`

• **OverView** : <em>{}</em>
"""

INLINE_DESC = """
**Usage:** `&lt;tv&gt; title` **or** `&lt;movie&gt; title` **in inline query.**

Examples:
× `&lt;movie&gt; Avengers Endgame`
× `&lt;tv&gt; Breaking Bad`
× `&lt;anime&gt; Attack on Titan`
• You can try on buttons below!
"""


# Start
START_STRING = """
Hey {}, I'm acutebot and i can help you to get \
information about your favorite movies, tv and anime shows, you can also download \
music & can view song lyrics using me! Just click the button \
below to get started with list of possible commands...

You can also search movies, tvshows & \
anime inline! just type `@acutebot` in \
your message box and follow the instructions.

And don't forget to smile, atleast once in a while ;)
"""
START_STRING_GRP = "Hmmm?"


# About
ABOUT_STR = f"""
I'm fully written in \
Python3 by <a href="tg://user?id=894380120">starry</a>, \
feel free to report him if you find any rough edge inside me.

**×** Bot version : `{__version__}`
**×** Python version : `{python_version()}`
**×** Library version : `PTB {_libv_}`
**×** Movies & TV data : `themoviedb.org`
**×** Anime data from : `kitsu.io`
**×** Music data from : `deezer.com`
**×** Lyrics data from : `genius.com`

If you enjoyed using me & wanna support my creator \
hit the donate button below, since he's just a student so \
every little helps to pay for my server, and ofcourse boosting morale ;)

"""

# Help
HELP_STR = """
Hey there, click on the buttons below to get documentations \
for the related functions.
"""

MOVIE_HELP = """
**🗒️ Documentation for Movies & TV related functions:**

**×** /movies : Search for info about your favorite movies.
**×** /tvshows : Get information for your favotite TV shows.
**×** /toprated : (Soon) | View information about top rated, Movie & TV titles.
"""
ANIME_HELP = """
**🗒️ Documentation for Anime & Manga related functionsfunctions:**

**×** /anime : Search for info about your favorite anime titles.
**×** /manga : Get information about your favorite manga titles.
"""
MUSIC_HELP = """
**🗒️ Documentation for music & lyrics related functions:**

**×** /music : Download your favorite music in high resolution.
**×** /lyrics : Get lyrics for your favorite songs.
**×** /nowplaying : Flex you currently or last played song in spotify.
"""
MISC_HELP = """
**🗒️ Documentation for some miscs command which don't fit anywhere!**

**×** /reddit : Gets you random memes scraped from popular subreddits.
**×** /subtitle : Download subtitles for your movies.
**×** /watchlist : Get list of saved shows from your watchlist :D.
"""

# Errors
API_ERR = "Sorry, couldn't reach API at the moment :("
NOT_FOUND = "Sorry, couldn't find any results for the query :("
INVALIDCAT = "Hmmm.. maybe you've sent wrong category to look for, please try again!"
KEYERROR = "Oops! something went wrong. Please try again :("

# Cancel
CANCEL = "Cancelled the current task!"

# To search
TOSEARCHMOVIE = "Please reply with the movie title you wanna look for."
TOSEARCHTV = "Please reply with the TV title you wanna look for."
TOSEARCH_ANIME = "Please reply with the anime title you want to look for."
TOSEARCH_MANGA = "Please reply with the manga name you wanna look for."

# Favs
NOFAVS = "Hmmm 🤔 looks like you don't have any title saved in your watchlist yet!"
REMFAV = "Great work! Successfully cleared your watchlist :)"
SAVED_FAV = "Added '{}' to your Watchlist!"
FAV_EXIST = (
    "Hey there this title is already in your watchlist, Go & finish it instead ;)"
)
NOT_ALLOWED = "The one who issued the command shall only click this holy button."

# Stats
STATS = """
📊 Current Stats;
👥 Total users : {}
💛 Watchlist saved : {}
"""

# Greet
GREET = "Hey {}! Thank you for adding me in {} :)"

# Lyrics
SONGNAME = "Please tell me name of the song you want lyrics for."
ARTISTNAME = "Great! now tell me name of the artist for this song."

LYRICS_ERR = """Sorry, looks like i forgot your song name, possibly due to restart \
Would you mind sending me again?
"""
LYRIC_NOT_FOUND = "Sorry i couldn't find lyrics for that song."
LYRICS_TOO_BIG = (
    "Lyrics of this song is too big for telegram, I'm sending it as a file..."
)

# Music
MUSICQ = "Please choose the quality of music :)"
MUSICNAME = "Okay! tell me name of the song you're looking for."
UPLOAD_BOTAPI = "⌛ uploading song please wait..."
UPLOAD_MTPROTO = "Hmm, file size is more than 50MBs, uploading via mtproto this might take around 5 mins, please wait..."
MUSICNOTFOUND = "Sorry i couldn't find that song :("

# Subtitles
TOSEARCHSUBS = "Please reply with the Movie | Anime name you want subs for."
SUBS_STR = "🏷 Subtitles for **{}**.\nClick on buttons below to download!"

# Spotify
SPT_LOGIN = "Hey {}, Please click the button below to login with your spotify account."
SPT_LOGIN_PM = "Please contact me in PM to login with your spotify account, inorder to use this feature."
