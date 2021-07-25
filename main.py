import os
import logging
import random
from sorular import D_LİST, C_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("Bot tokeniniz") # Kullanıcı'nın Bot Tokeni
API_HASH = os.getenv("api hash") # Kullanıcı'nın Apı Hash'ı
OWNER_ID= (1801589805)

MOD = None

logging.basicConfig(level=logging.INFO)
#+++++++++++++++++++++++++++++++++++++++++++++++++++
bot = Client(
    "my_account",
    api_id=7140664,
    api_hash="414c9a58b4a95e30a4e29608626e148f",
    bot_token="1837191913:AAHgdApg8rji8Ga6lGku1wlrj6AmE7WMLts"
)

def button():
	BUTTON=[[InlineKeyboardButton(text="Kanalımız",url="t.me/GroupMasterRobotOfficial")]]
	return InlineKeyboardMarkup(BUTTON)

@bot.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="**Salam dostum*\n\n__Mən doğruluq və cəsarət botuyam __\nOyunu qrupda başlatmaq üçün /game yazın".format(
		user.mention,
		),
	disable_web_page_preview=True, 
	reply_markup=button()
	)

def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="Doğruluq", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="Cəsarət", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

@bot.on_message(filters.command("game"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} Doğruluq yoxsa cəsarət!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

@bot.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LİST)
	c_soru=random.choice(C_LİST)
	user = callback_query.from_user

	c_q_d, user_id = callback_query.data.split()

		if c_q_d == "d_data":
			await callback_query.answer(text="Siz doğruluğu seçdiz\n", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)

			await callback_query.message.reply_text("**{user} doğruluq sualın gəldi!:**\n\n__{d_soru}__".format(user=user.mention, d_soru=d_soru))
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Sizcəsarət seçdiz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cəsarət sualın gəldi. Xaiş olunur suala əməl et!:**\n\n__{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return

	else:
		await callback_query.answer(text="Bu əmri sən verməmisən!!", show_alert=False)
		return

@bot.on_message(filters.command("cet"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**Sən bot sahiblsən deyilsən!!**")
    return
  MOD="cet"
  await message.reply_text("**Əlavə etmək istədiyiniz sualı yazın!!**")
  
@bot.on_message(filters.command("det"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**Sən bot sahiblsən deyilsən!!**")
    return
  MOD="cekle"
  await message.reply_text("**Əlavə etmək istədiyiniz sualı yazın!!**")

@bot.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_LİST
  global D_LİST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("Cəsarət sualı əlavə oldundu!!")
      return
    if MOD=="dekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("Doğruluq sualı əlavə oldundu!!")
      return

bot.run()