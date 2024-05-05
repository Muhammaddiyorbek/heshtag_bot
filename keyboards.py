from aiogram.types import *
from aiogram import Bot


def asosy_menu(user_id,adminlarDb_data):
    lis=[
        [
            InlineKeyboardButton(text="🔗 Referal",callback_data='referal'),
            InlineKeyboardButton(text='#️⃣ Heshtag Generated 🔄',callback_data='heshtag_generated')
        ],
        [
            InlineKeyboardButton(text="Imkoniyatlarni ko'rish 👁️",callback_data='imkon_korish')
        ]  
    ]
    if user_id in adminlarDb_data:
        lis.append([InlineKeyboardButton(text="👨‍💻 Admin panel",callback_data='admin_panel')])
    return InlineKeyboardMarkup(
        inline_keyboard=lis
    )

def admin_panel():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🆕 Admin Qo'shish ➕",callback_data='admin_qoshish'),
                InlineKeyboardButton(text="🗑 Admin O'chirish ❌",callback_data='admin_ochirish'),
            ],
            [
                InlineKeyboardButton(text="🆕 Heshtag Qo'shish ➕",callback_data='heshtag_qoshish'),
                InlineKeyboardButton(text="🆕 Tayyor Heshtag ➕",callback_data='tayyor_heshtag'),
            ],
            [
                InlineKeyboardButton(text="📈 Statistika 📊",callback_data='statistica'),
                InlineKeyboardButton(text="🗑 Heshtag O'chirish ❌",callback_data='heshtag_ochirish'),
            ],
            [
                InlineKeyboardButton(text='📜 Heshtaglarni ko\'rish 👁️',callback_data="heshtag_korish")
            ],
            [
                InlineKeyboardButton(text='🗣 Reklama Soqqa 💰',callback_data="reklama"),
                InlineKeyboardButton(text='✏️ Imkon 💵',callback_data="imokon_tahrirlash"),
            ],
            [
                InlineKeyboardButton(text="🆕 Kanal Qo'shish ➕",callback_data='kanal_qoshish'),
                InlineKeyboardButton(text="🗑 Kanal O'chirish ❌",callback_data='kanal_ochirish'),
            ],
        ]
    )

def delete_utton():
    return ReplyKeyboardRemove()

def heshtagOchirishinlineButton(heshtag_data):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🆔{h[0]} - #️⃣{h[-1][:20]}",callback_data=f"del_h{h[0]}")] for h in heshtag_data
        ]
    )

def get_all_user_info():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="All User Info",callback_data="all_user_info")
            ]
        ]
    )

async def is_obuna_button(user_id,kanallarDb_data,bot:Bot):
    lis=[]
    kanal_sanash=1
    for i in kanallarDb_data:
        try:
            kanal=await bot.get_chat(i)
            status=await bot.get_chat_member(chat_id=kanal.id,user_id=user_id)
            if status.status in ["left","kicked"]:
                lis.append([InlineKeyboardButton(text=f"№ {kanal_sanash} - {kanal.title}",url=kanal.invite_link)])
                kanal_sanash+=1
        except Exception as e:
            print(e)
    return lis

def admin_ochirish(admin_data):
    lis=[[InlineKeyboardButton(text=str(admin),callback_data=f"del_a{admin}")] for admin in admin_data]
    return InlineKeyboardMarkup(
        inline_keyboard=lis
    )

def kanal_ochirish(kanal_data):
    lis=[[InlineKeyboardButton(text=str(kanal),callback_data=f"del_k{kanal}")] for kanal in kanal_data]
    return InlineKeyboardMarkup(
        inline_keyboard=lis
    )

def configImkon(userDb_data):
    lis=[[InlineKeyboardButton(text=str(user[1]),callback_data=f"imkon_c{user[0]}")] for user in userDb_data]
    return InlineKeyboardMarkup(
        inline_keyboard=lis
    )