
from pyrogram import Client,filters, enums, __version__
# from bot import Bot
from config import STREAM_LOGS
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash
from config import *
from html import escape
import hashlib
import hmac
from script import Script
# Define a secret key for hash generation (keep it private!)
SECRET_KEY = "the_one_and_only_lazydeveloper"  # Replace with a strong, unique key

def validate_hash(log_msg_id, provided_hash):
    """
    Validate the provided hash against the expected hash for the given log_msg_id.
    """
    # Generate the expected hash for the given log_msg_id
    expected_hash = generate_hash(log_msg_id)

    # Compare the provided hash with the expected hash
    return hmac.compare_digest(expected_hash, provided_hash)


def generate_hash(message_id: int) -> str:
    """
    Generate a secure hash from the message ID.
    """
    # Convert the message ID to a string and hash it
    return hashlib.sha256(str(message_id).encode('utf-8')).hexdigest()[:6]  # First 6 characters


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=Script.START_MSG.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [
                InlineKeyboardButton('♻ᴜᴘᴅᴀᴛᴇꜱ ', url='https://telegram.me/cricketclipsprovider'),
                InlineKeyboardButton('🧩ꜱᴜᴘᴘᴏʀᴛ ', url='https://telegram.me/cricketclipsprovider')
                ],[
                InlineKeyboardButton("👑 • ᴏᴡɴᴇʀ • 💎", callback_data='own')
                ],[
                InlineKeyboardButton("❤ • ᴅᴇᴠ • 🍟", callback_data='dev')
                ],[
                InlineKeyboardButton('🤚ᴀʙᴏᴜᴛ ', callback_data='about'),
                InlineKeyboardButton('❓ ʜᴇʟᴘ ❓', callback_data='help')
                ]]),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
    elif data == "help":
        await query.message.edit_text(
            text=Script.HELP_TEXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [
                InlineKeyboardButton("🔒 ᴄʟᴏꜱᴇ •", callback_data = "close"),
                InlineKeyboardButton("◀️ ʙᴀᴄᴋ •", callback_data = "start")
               ]
               ]
            ),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif data == "about":
        await query.message.edit_text(
            text=Script.ABOUT_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("🔒 ᴄʟᴏꜱᴇ •", callback_data = "close"),
                InlineKeyboardButton("◀️ ʙᴀᴄᴋ •", callback_data = "start")
               ]]
            ),
            parse_mode=enums.ParseMode.HTML
        )
    elif data == "dev":
        
        await query.message.edit_text(
            text=Script.DEVELOPER_TEXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("🔒 ᴄʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data = "start")
               ]]
            ),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML 
        )

    elif data == "own":
        await query.message.edit_text(
            text=Script.OWNER_TEXT.format(TEL_USERNAME, TEL_NAME),
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("🔒 ᴄʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data = "start")
               ]]
            ),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif data.startswith("generate_stream_link"):
        # _, fileid = data.split(":")
        try:
            xo = await query.message.reply_text(f'🔐')
            user_id = query.from_user.id
            username =  query.from_user.mention 
            new_text = query.message.text
            # Directly access the file from the callback query's associated message
            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            file_id = file.file_id
            # file_name = quote_plus(file.file_name)

            log_msg = await client.send_cached_media(
                chat_id=STREAM_LOGS, 
                file_id=file_id,
            )

            fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ  🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>\n🧩User Id: {user_id} \n👮‍♂️ UserName: {username}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('▶Stream online', url=lazy_stream)]])  # web stream Link
            )
            
            await query.message.edit_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ 🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                        InlineKeyboardButton('▶Stream online', url=lazy_stream)
                    ],
                    ])  # web stream Link
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong sweetheart\n\n{e}", show_alert=True)
            return 
 
    elif data.startswith("convert_link"):
        try:
            xo = await query.message.reply_text(f'🔐')
            
            original_link = query.message.reply_to_message

            log_msg = await client.send_message(
                chat_id=STREAM_LOGS, 
                text=f"{original_link.text}",
            )

            unique_id = generate_hash(log_msg.id)
            target_url = original_link.text
            stream_url = f"{URL}play/{unique_id}/{log_msg.id}"
            reply_button = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📺 Stream Now 🎥", url=stream_url)
                ]
            ])
            await log_msg.edit_text(
                f"{target_url}\n\n<blockquote><b>🧩ᴜɴɪǫᴜᴇ-ɪᴅ<b>: <code>{unique_id}</code> </blockquote>\n<b>👮‍♂️ɢᴇɴᴇʀᴀᴛᴇᴅ-ʙʏ</b>\n<blockquote><b>👩‍💻ɴᴀᴍᴇ:</b> {query.from_user.mention}\n<b>🆔ɪᴅ:</b> {query.from_user.id} </blockquote>\n<blockquote>📱<b>ɢᴇɴᴇʀᴀᴛᴇᴅ ʟɪɴᴋ:<b> {stream_url}</b></blockquote>\n<blockquote>🗑ʀᴇᴠᴏᴋᴇ ʟɪɴᴋ :\n/revoke {unique_id}</blockquote>\n\n<blockquote>⚠ᴅᴏn'ᴛ ᴅᴇʟᴇᴛᴇ/ᴇᴅɪᴛ ᴛʜɪs ᴘᴏsᴛ🚮</blockquote>",
                    reply_markup=reply_button)
            await asyncio.sleep(1)
            await xo.delete()
            replybtn = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={stream_url}')],
                ]
            )
            await query.message.edit(
                text=f"✅ ʜᴇʏ {query.from_user.mention}, ʏᴏᴜʀ sᴛʀᴇᴀᴍᴀʙʟᴇ ʟɪɴᴋ ɪs ʀᴇᴀᴅʏ:\n\n🍟 ᴡᴀᴛᴄʜ ɴᴏᴡ: {stream_url}",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=replybtn
            )
            await asyncio.sleep(1)
            await client.send_message(
                    chat_id=STREAM_LOGS,
                    text=f"🎒 ᴄᴏɴᴠᴇʀᴛᴇᴅ ʟɪɴᴋ ғᴏʀ ᴜsᴇʀ:\n<blockquote>🔗 Original: {target_url}</blockquote>\n<blockquote>🌐 Stream: {stream_url}</blockquote>"
                )
            
            await query.answer("🎒 ʟɪɴᴋ ᴄᴏɴᴠᴇʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!\nᴘᴏᴡᴇʀᴇᴅ ʙʏ ʟᴀᴢʏᴅᴇᴠᴇʟᴏᴘᴇʀ🍟")
        except Exception as e:
            print(e)
            await query.answer(f"☣ Unable to generate  link\n\n{e}", show_alert=True)

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

