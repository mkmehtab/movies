from pyrogram import Client, filters
from search import search_movies

# Telegram Bot Credentials
API_ID = 22470161
API_HASH = "1360539223d4b5c2eecad27f9cac40c5"
BOT_TOKEN = "7733173048:AAH1_jZLbZqqMzAHZiqQ110JXPe9WoSnqIY"

app = Client(
    "movie_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.private & filters.text)
async def movie_handler(client, message):
    query = message.text
    results = search_movies(query)

    if not results:
        await message.reply("Movie not found on KatmovieHD or HDHub4u.")
        return

    for movie in results:
        text = f"**{movie['title']}**\nSource: `{movie['source']}`\n\n{movie['description']}\n\n"
        for i, link in enumerate(movie['downloads'], 1):
            text += f"[Download {i}]({link})\n"
        await message.reply(text, disable_web_page_preview=True)

app.run()
