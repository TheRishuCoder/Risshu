import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from config import PLAYLIST_IMG_URL, adminlist
from strings import get_string
from VIPMUSIC import YouTube, app
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.utils.database import (get_cmode, get_lang, get_assistant,
                                       get_playmode, get_playtype,
                                       is_active_chat,
                                       is_served_private_chat)
from VIPMUSIC.utils.database import is_maintenance
from VIPMUSIC.utils.inline.playlist import botplaylist_markup


    # This function is not defined in the provided code, so it needs to be implemented

def PlayWrapper(command):
    async def wrapper(client, message):
        chat_id = message.chat.id
        userbot = await get_assistant(message.chat.id)
        userbot_id = userbot.id
        
        # Get chat member object
        chat_member = await app.get_chat_member(chat_id, app.id)
        
        # Condition 1: Group username is present, bot is not admin
        if message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            try:
                await userbot.join_chat(message.chat.username)
            except Exception as e:
                return await message.reply("**ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ᴜɴʙᴀɴ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ!**")
                pass
        # Condition 2: Group username is present, bot is admin, and Userbot is not banned
        if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            try:
                await userbot.join_chat(message.chat.username)
            except Exception as e:
                return await message.reply(str(e))
                pass
        # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
        if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            userbot_member = await app.get_chat_member(chat_id, userbot.id)
            if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                    await userbot.join_chat(message.chat.username)
                except Exception as e:
                    return await message.reply("**ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ, ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ʙᴀɴ ᴘᴏᴡᴇʀ ᴀɴᴅ ɪɴᴠɪᴛᴇ ᴜsᴇʀ ᴘᴏᴡᴇʀ ᴏʀ ᴜɴʙᴀɴ ᴀssɪsᴛᴀɴᴛ ᴍᴀɴᴜᴀʟʟʏ ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ ʙʏ /userbotjoin**")
                    pass
        # Condition 4: Group username is not present/group is private, bot is not admin
        if not message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.reply("**ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ.**")
            pass
        # Condition 5: Group username is not present/group is private, bot is admin
        if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            try:
                userbot_member = await app.get_chat_member(chat_id, userbot.id)
                if userbot_member.status not in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                    await message.reply("")
            except Exception as e:
                ok = await message.reply("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ**.")
                invite_link = await app.create_chat_invite_link(chat_id, expire_date=None)
                await asyncio.sleep(1)
                await userbot.join_chat(invite_link.invite_link)
                await ok.delete()
            except Exception as e:
                return await message.reply(f"**➻ ᴀᴄᴛᴜᴀʟʟʏ ɪ ғᴏᴜɴᴅ ᴛʜᴀᴛ ᴍʏ ᴀssɪsᴛᴀɴᴛ ʜᴀs ɴᴏᴛ ᴊᴏɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ ʙᴇᴄᴀᴜsᴇ [ ɪ ᴅᴏɴᴛ ʜᴀᴠᴇ  ɪɴᴠɪᴛᴇ ᴜsᴇʀ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ] sᴏ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ ʙʏ- /userbotjoin.**\n\n**➥ ɪᴅ »** @{userbot.username}")
                pass
        # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
        if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            userbot_member = await app.get_chat_member(chat_id, userbot.id)
            if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                    invite_link = await app.create_chat_invite_link(chat_id, expire_date=None)
                    await asyncio.sleep(1)
                    await userbot.join_chat(invite_link.invite_link)
                except Exception as e:
                    return await message.reply(f"**➻ ᴀᴄᴛᴜᴀʟʟʏ ɪ ғᴏᴜɴᴅ ᴛʜᴀᴛ ᴍʏ ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ᴜɴʙᴀɴ ᴍʏ ᴀssɪsᴛᴀɴᴛ ʙᴇᴄᴀᴜsᴇ [ ɪ ᴅᴏɴᴛ ʜᴀᴠᴇ  ʙᴀɴ ᴘᴏᴡᴇʀ ] sᴏ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ʙᴀɴ ᴘᴏᴡᴇʀ ᴏʀ ᴜɴʙᴀɴ ᴍʏ ᴀssɪsᴛᴀɴᴛ ᴍᴀɴᴜᴀʟʟʏ ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ ʙʏ- /userbotjoin.**\n\n**➥ ɪᴅ »** @{userbot.username}")
                    pass
       
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "» ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ғᴏʀ sᴏᴍᴇ ᴛɪᴍᴇ, ᴩʟᴇᴀsᴇ ᴠɪsɪᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇ ʀᴇᴀsᴏɴ..."
                )
        
        
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        audio_telegram = (
            (
                message.reply_to_message.audio
                or message.reply_to_message.voice
            )
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (
                message.reply_to_message.video
                or message.reply_to_message.document
            )
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)
        if (
            audio_telegram is None
            and video_telegram is None
            and url is None
        ):
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ʜᴏᴡ ᴛᴏ ғɪx ᴛʜɪs ?",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                _["general_4"], reply_markup=upl
            )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
