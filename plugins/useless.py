# from bot import Bot
from pyrogram import filters, Client
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import hashlib
from config import *
from database.database import present_user, add_user

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


# @Client.on_message(filters.private & filters.incoming)
# async def useless(_,message: Message):
#     if USER_REPLY_TEXT:
#         await message.reply(USER_REPLY_TEXT)




# Dictionary to temporarily store links



@Client.on_message(filters.private & filters.text & ~filters.command(['stats', 'broadcast', 'users', 'start', 'revoke', 'add_admin', 'remove_admin', 'view_admin_list']))
async def receive_link(client: Client, message: Message):
    """
    Handle when the user sends a link to the bot.
    """
    user_id = message.from_user.id
    link = message.text.strip()
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    # Validate link format (basic validation)
    if not link.startswith("http"):
        await message.reply("❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ. ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴜʀʟ.")
        return

    # Forward the link to the Stream Log Channel
    log_message = await client.send_message(
        chat_id=STREAM_LOGS,
        text=f"🔗 ʀᴇᴄᴇɪᴠᴇᴅ ʟɪɴᴋ ғʀᴏᴍ ᴜsᴇʀ\n<blockquote>ID: {user_id}\n👮‍♂️ɴᴀᴍᴇ: {message.from_user.mention}</blockquote>\n<blockquote><code>{link}</code></blockquote>"
    )

    # Store the link in the dictionary using the log message ID as a reference
    # stream_links[log_message.id] = link

    # Send a button to the user to convert the link
    await message.reply_text(
        text=f"✅ ʟɪɴᴋ ʀᴇᴄᴇɪᴠᴇᴅ! ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ᴛᴏ ᴀ sᴛʀᴇᴀᴍᴀʙʟᴇ ʟɪɴᴋ.\n\n⚠ᴘʟᴇᴀsᴇ ʀᴇᴄʜᴇᴄᴋ ʏᴏᴜʀ ʟɪɴᴋ ʙᴇғᴏʀᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴡᴀᴛᴄʜ ʟɪɴᴋ...\n<blockquote>🔗 {link}</blockquote>",
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📺ᴄᴏɴᴠᴇʀᴛ ᴛᴏ sᴛʀᴇᴀᴍ ʟɪɴᴋ📺", callback_data=f"convert_link")]]
        )
    )

