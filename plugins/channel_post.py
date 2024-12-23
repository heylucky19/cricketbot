
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# from bot import Bot
from config import *
from helper_func import encode
from database.database import present_user, add_user

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{BOT_USERNAME}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("📂 ᴅᴏᴡɴʟᴏᴀᴅ / sᴛʀᴇᴀᴍ 🍿", callback_data=f'generate_stream_link')],
        ]
        )

    await reply_text.edit(f"<b>📂 ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ʟɪɴᴋ:</b>\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    # if not DISABLE_CHANNEL_BUTTON:
    #     await post_message.edit_reply_markup(reply_markup)

@Client.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{BOT_USERNAME}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
