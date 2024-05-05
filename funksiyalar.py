from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,CallbackQuery
from keyboards import *
from sql_file import *
import random
from fsm_form import *
import time

bot_link="https://t.me/instagram_heshtag_bot"
userDb=User('users')
heshtagDb=Heshteglar('heshteglar')
adminlarDb=Adminlar('adminlar')
kanallarDb=Kanallar('kanallar')


def generate_referal(user_id):
    return f"{bot_link}?start={user_id}"

def chek_admin(user_id):
    if user_id in adminlarDb.getAdminId():
        return True
    return False

async def get_user(user_id,bot:Bot):
    try:return await bot.get_chat(chat_id=user_id)
    except:return False

def generate_heshtag(user_id):
    if heshtagDb.getSQL():
        userDb.configImkon(user_id=user_id,imkon_type=userDb.getImkon(user_id)-1)
        return random.choice(heshtagDb.getSQL())[-1]
    return "None"
# ##########################################
async def start(mes:Message,bot:Bot):
    mes_text=mes.text.split(' ')
    my_user=mes.from_user
    if len(mes_text)==2 and await get_user(mes_text[-1],bot) and (not userDb.getSQL(mes.from_user.id)):
        user=await get_user(mes_text[-1],bot)
        if user.id == mes.from_user.id:
            await mes.answer("O'zingizga referal bola olmaysiz")
            if not userDb.getSQL(mes.from_user.id):
                userDb.addUser(full_name=my_user.full_name,user_id=my_user.id,my_referal='None',imkon=0)
            return
        elif user.id not in userDb.getAllUserId():
            await mes.answer("Noto'g'ri referal")
            if not userDb.getSQL(mes.from_user.id):
                userDb.addUser(full_name=my_user.full_name,user_id=my_user.id,my_referal='None',imkon=0)
            return
        await mes.answer(f"Sizni <a href='tg://user?id={user.id}'>{user.full_name}</a> taklif qildi")
        userDb.addUser(full_name=my_user.full_name,user_id=my_user.id,my_referal=user.id,imkon=0)
        userDb.configImkon(user_id=user.id,imkon_type=userDb.getImkon(user.id)+1)
        await bot.send_message(user.id,f"Siz taklif qilgan <a href='tg://user?id={my_user.id}' >{my_user.full_name}</a> botga qo'shildi!\n\nSizga +1 imkoniyat qo'shildi")
    await mes.answer("Assalomu alaykum botga hush kelibsiz")
    await mes.answer("Tugmalardan birini tanlang",reply_markup=asosy_menu(my_user.id,adminlarDb.getAdminId()))
    if not userDb.getSQL(mes.from_user.id):
        userDb.addUser(full_name=my_user.full_name,user_id=my_user.id,my_referal='None',imkon=0)
    await mes.delete()


async def generateReferal(cal:CallbackQuery,bot:Bot):
    user_id=cal.message.chat.id
    if await is_obuna_button(user_id,kanallarDb.getKanalLink(),bot):
        await cal.answer()
        await cal.message.answer("Botdan foydalanish uchun Kanalga obuna bo'ling",reply_markup=InlineKeyboardMarkup(inline_keyboard=await is_obuna_button(user_id,kanallarDb.getKanalLink(),bot)))
    else:
        await cal.answer("Referal yaratilmoqda")
        referal=generate_referal(cal.message.chat.id)
        await cal.message.answer("Sizning referal havolangiz\n\n"+referal)
    

async def imkoniyatniKorish(cal:CallbackQuery):
    await cal.answer("Imkoniyatni ko'rish")
    imkoniyat=userDb.getImkon(user_id=cal.message.chat.id)
    await cal.message.answer(f"Sizning imkoniyatingiz: {imkoniyat} ta")

async def generateHeshtag(cal:CallbackQuery,bot:Bot):
    if int(userDb.getImkon(cal.message.chat.id))>0:
        user_id=cal.message.chat.id
        if await is_obuna_button(user_id,kanallarDb.getKanalLink(),bot):
            await cal.answer()
            await cal.message.answer("Botdan foydalanish uchun Kanalga obuna bo'ling",reply_markup=InlineKeyboardMarkup(inline_keyboard=await is_obuna_button(user_id,kanallarDb.getKanalLink(),bot)))
        else:
            await cal.answer("Heshtag yaratilmoqda")
            heshtag=generate_heshtag(cal.message.chat.id)
            await cal.message.answer(f"Sizning heshtagingiz:\n\n<code>{heshtag}</code>")
    else:
        await cal.answer()
        await cal.message.answer(f"Sizning imkoniyatingiz qolmagan!\nImkoniyatni ko'paytirish uchun referal orqali do'stingizni taklif qiling. \n\n{generate_referal(cal.message.chat.id)}")
# ---------------(admin)-------------------
async def adminPanel(cal:CallbackQuery):
    user_id=cal.message.chat.id
    await cal.answer()
    if user_id in adminlarDb.getAdminId():await cal.message.answer("Admin Panel",reply_markup=admin_panel())
    else:await cal.message.answer("Siz admin emasiz!")

#-----------(reklama)-------------   
async def setReklama(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Reklama yuboring..")
    await state.set_state(ReklamaForm.reklama)

async def getReklama(mes:Message,bot:Bot,state:FSMContext):
    for i in userDb.getAllUserId():
        try:
            time.sleep(0.5)
            await bot.forward_message(i,mes.from_user.id,mes.message_id)
        except Exception as e:
            print(e)
    await mes.answer("Reklama barcha foydalanuvchilarga yuborildi ✅")
    await mes.answer("Admin Panel",reply_markup=admin_panel())
    await state.clear()
# ----------(admin[+,-])-----------------
async def setAdminQoshish(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Admin <b>ID</b>sini kiriting...")
    await state.set_state(AdminForm.admin_qoshish)

async def getAdminQoshish(mes:Message,state:FSMContext,bot:Bot):
    try:
        admin_user=await bot.get_chat(mes.text)
        if chek_admin(mes.from_user.id) and adminlarDb.addSQL(admin_link=admin_user.username if admin_user.username else admin_user.full_name,admin_id=admin_user.id):
            await mes.answer("Admin qo'shildi ✅")
            await state.clear()
            await mes.answer("Admin Panel",reply_markup=admin_panel())
        else:
            await mes.answer("Bunday admin mavjud!")
    except:
        await mes.answer("Xatolik yuz berdi!")

async def setAdminOchirish(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Qaysi Adminni o'chirmoqchisiz?",reply_markup=admin_ochirish(adminlarDb.getAdminLink()))

async def getAdminOchirish(cal:CallbackQuery):
    data=cal.data.replace("del_a","")
    await cal.answer()
    if "Developer_Flutter_Uz"!=data:adminlarDb.deleteSQL(admin_link=data)
    await cal.message.answer("Admin o'chirildi ✅")
# ---------(kanal[+,-])--------------
async def setKanalQoshish(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Kanal <b>Link</b>ini kiriting...")
    await state.set_state(KanalForm.kanal_qoshish)

async def getKanalQoshish(mes:Message,state:FSMContext,bot:Bot):
    kanallarDb.addSQL('@'+mes.text.replace("https://t.me/","").replace('@',""))
    await mes.answer("Kanal qo'shildi ✅")

async def setKanalOchirish(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Qaysi Kanaldi o'chirmoqchisiz?",reply_markup=kanal_ochirish(kanallarDb.getKanalLink()))

async def getKanalOchirish(cal:CallbackQuery):
    data=cal.data.replace("del_k","")
    await cal.answer()
    kanallarDb.deleteSQL(kanal_link=data)
    await cal.message.answer("Kanal o'chirildi ✅")

async def setHeshtagQoshish(cal:CallbackQuery,state:FSMContext):
    await cal.message.answer("Heshtag kiriting ...📝")
    await cal.message.delete()
    await state.set_state(HeshtagForm.heshtag_qoshish)

async def setHeshtagTayyor(cal:CallbackQuery,state:FSMContext):
    await cal.message.answer("Heshtag kiriting ...📝")
    await cal.message.delete()
    await state.set_state(HeshtagForm.heshtag_qoshish_tayyor)

async def getHeshtagQoshish(mes:Message,state:FSMContext):
    heshtag_text=""
    text=mes.text.split(' ')
    tek=0
    for t in text:
        if tek!=3:
            heshtag_text+=f"#{t} "
        else:
            heshtag_text+=f"\n#{t} "
            tek=0
        tek+=1
    heshtagDb.addSQL(heshteg=heshtag_text)
    await mes.answer("Heshtag qo'shildi ✅")
    await mes.answer("Admin Panel",reply_markup=admin_panel())
    await state.clear()

async def getHeshtagTayyor(mes:Message,state:FSMContext):
    heshtag_text=mes.text
    heshtagDb.addSQL(heshteg=heshtag_text)
    await mes.answer("Heshtag qo'shildi ✅")
    await mes.answer("Admin Panel",reply_markup=admin_panel())
    await state.clear()

async def heshtagKorish(cal:CallbackQuery):
    await cal.answer()
    if heshtagDb.getSQL():
        for heshtag in heshtagDb.getSQL():await cal.message.answer(f"🆔: {heshtag[0]}\n\n#️⃣: <code>{heshtag[-1]}</code>")
    else:await cal.message.answer("Heshtaglar yo'q")
    
async def heshtagOchirish(cal:CallbackQuery):
    await cal.answer()
    if heshtagDb.getSQL():
        await cal.message.answer("Qaysi heshtagni o'chirishni hohlaysiz?",reply_markup=heshtagOchirishinlineButton(heshtagDb.getSQL()))
    else:
        await cal.message.answer("Heshtaglar yo'q")

async def heshtagOchirishSQL(cal:CallbackQuery):
    await cal.answer()
    heshtag_id=int(cal.data.replace("del_h",""))
    heshtagDb.deleteSQL(heshteg_id=heshtag_id)
    await cal.message.answer("Heshtag o'chirildi ✅")
    await cal.message.delete()
    await cal.message.answer("Admin Panel",reply_markup=admin_panel())

async def statistikaKorish(cal:CallbackQuery):
    await cal.answer()
    users=userDb.getAllUsers()
    hashtags=heshtagDb.getSQL()
    all_info=f"<b>Foydalanuvchilar soni: {len(users)} ta</b>\n\n"
    all_info+=f"<b>Heshtaglar soni: {len(hashtags)}</b>\n\n"
    await cal.message.answer(all_info,reply_markup=get_all_user_info())

async def allUserInfo(cal:CallbackQuery):
    await cal.answer()
    all_user_info=""
    for index,user in enumerate(userDb.getAllUsers(),start=1):
        all_user_info+=f"{index}) <a href='tg://user?id={user[0]}'>{user[1]}</a> - imkoniyati: {user[-1]} ta\n"
    await cal.message.answer(all_user_info)

async def setImkonTahrirlash(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    await cal.message.answer("Qaysi Foydalanuvchini Imkoniyatini o'zgartirmoqchisiz?",reply_markup=configImkon(userDb.getAllUsers()))
        
async def getImkonTahrirlash(cal:CallbackQuery,state:FSMContext):
    await cal.answer()
    user_id=int(cal.data.replace("imkon_c",""))
    await cal.message.answer(f"Foydalanuvchi <a href='tg://user?id={user_id}'>{userDb.getSQL(user_id)[1]}</a> imkoniyati {userDb.getSQL(user_id)[-1]} ta\nImkoniyatini kiriting...")
    await state.update_data(imkon_tahrirlash=user_id)
    await state.set_state(ImkonForm.imkon_tahrirlash)

async def getImkonTahrirlash2(mes:Message,state:FSMContext):
    user_id=await state.get_data()
    try:
        imkon=int(mes.text)
        userDb.configImkon(user_id=user_id['imkon_tahrirlash'],imkon_type=imkon)
        await mes.answer("Imkoniyat o'zgartirildi ✅")
        await mes.answer("Admin Panel",reply_markup=admin_panel())
        await state.clear()
    except:
        await mes.answer("Xatolik yuz berdi!")