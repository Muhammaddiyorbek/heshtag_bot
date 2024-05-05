from aiogram import Dispatcher,Bot,F
from funksiyalar import *
from aiogram.filters import Command,and_f
import asyncio
from fsm_form import HeshtagForm

bot_token="6861475559:AAFIfTg9r6O8Qt2EWKGuCVAY6Kj-vU96gxE"

async def main():
    bot=Bot(bot_token,parse_mode="HTML")
    dp=Dispatcher()
    dp.message.register(start,Command('start'))
    dp.callback_query.register(generateReferal,F.data=="referal")
    dp.callback_query.register(imkoniyatniKorish,F.data=="imkon_korish")
    dp.callback_query.register(generateHeshtag,F.data=="heshtag_generated")
    # -----------(admin)----------------
    dp.callback_query.register(adminPanel,F.data=="admin_panel")
    dp.callback_query.register(setHeshtagQoshish,F.data=="heshtag_qoshish")
    dp.callback_query.register(setHeshtagTayyor,F.data=="tayyor_heshtag")
    dp.callback_query.register(setReklama,F.data=="reklama")
    dp.message.register(getReklama,ReklamaForm.reklama)
    dp.message.register(getHeshtagQoshish,HeshtagForm.heshtag_qoshish)
    dp.message.register(getHeshtagTayyor,HeshtagForm.heshtag_qoshish_tayyor)
    dp.callback_query.register(heshtagKorish,F.data=="heshtag_korish")
    dp.callback_query.register(heshtagOchirish,F.data=="heshtag_ochirish")
    dp.callback_query.register(heshtagOchirishSQL,F.data.startswith("del_h"))
    dp.callback_query.register(statistikaKorish,F.data=="statistica")
    dp.callback_query.register(allUserInfo,F.data=="all_user_info")
    dp.callback_query.register(setAdminQoshish,F.data=="admin_qoshish")
    dp.message.register(getAdminQoshish,AdminForm.admin_qoshish)
    dp.callback_query.register(setAdminOchirish,F.data=="admin_ochirish")
    dp.callback_query.register(getAdminOchirish,F.data.startswith("del_a"))
    dp.callback_query.register(setKanalQoshish,F.data=="kanal_qoshish")
    dp.message.register(getKanalQoshish,KanalForm.kanal_qoshish)
    dp.callback_query.register(setKanalOchirish,F.data=="kanal_ochirish")
    dp.callback_query.register(getKanalOchirish,F.data.startswith("del_k"))
    dp.callback_query.register(setImkonTahrirlash,F.data.startswith("imokon_tahrirlash"))
    dp.callback_query.register(getImkonTahrirlash,F.data.startswith("imkon_c"))
    dp.message.register(getImkonTahrirlash2,ImkonForm.imkon_tahrirlash)
    try:
        await dp.start_polling(bot)
    except Exception as error:
        print(error)

if __name__=="__main__":
    asyncio.run(main())
