import telebot
import wikipedia
import json
from button import InlineKeyboardButton,KeyboardButton


bot = telebot.TeleBot("BOT_TOKEN")

# json faylga ma'lumot qo'shish
def royxatdan_otish(message):
    return {
        'id': message.from_user.id,
        'ism': message.from_user.first_name,
        'username': message.from_user.username,
        'contact': message.contact.phone_number,
    }

def saqlangan_malumotlar(foydalanuvchi):
    royxat = []
    try:
        with open('foydalanuvchilar.json', 'r') as fayl:
            royxat = json.load(fayl)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass

    if foydalanuvchi not in royxat:
        royxat.append(foydalanuvchi)

    with open('foydalanuvchilar.json', 'w') as fayl:
        json.dump(royxat, fayl, indent=2)

# Botni ishga tushirish
@bot.message_handler(commands=['start'])
def send_welcome(message = ['start']):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Telefon raqamni yuborish", request_contact=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, """Assalomu alaykum ☺️
                 
⬇️ Kontaktingizni yuboring ⬇️""", reply_markup=keyboard)

# Buttonlarni chiqarish
@bot.message_handler(content_types=['contact'])
def contact_received(message):
    contact = message.contact
    foydalanuvchi = royxatdan_otish(message)
    saqlangan_malumotlar(foydalanuvchi)
    
    markup = KeyboardButton().create_button_keyboard()
    bot.send_message(message.chat.id, "🇷🇺Выберите язык/🇺🇿Tilni tanlang/🇺🇸Select a language", reply_markup=markup)

# Help commanda
@bot.message_handler(commands=['help'])
def send_help(message=['help']):
    
    bot.send_message(message.chat.id, """
📌 Buyruqlar

Shunchaki menga biror bir maqola nomini qisqacha 
qilib yuboring va men sizga topib berishga harakat qilaman.
Misol uchun: (Toshkent shahri, Python tili, Alisher Navoiy)
/start-botni ishlatish
/language-tilni o'zgartirish

Bot ishlashi bo'yicha taklif va shikoyatlatlar
bo'lsa Adminga bog'laning ⬇️

Bog'lanish uchun aloqa: @developer_000                    
    """)

# Language commanda(tilni almashtiradi)
@bot.message_handler(commands=['language'])
def send_language(message=['language']):
    markup = KeyboardButton().create_button_keyboard()
    
    bot.send_message(message.chat.id, "🇷🇺Выберите язык/🇺🇿Tilni tanlang/🇺🇸Select a language", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'Русский':
        wikipedia.set_lang("ru")
        bot.send_message(call.message.chat.id, """
Вы выбрали русский 🇷🇺

Напишите тему статьи ⬇️ """)
    elif call.data == 'Uzbek':
        wikipedia.set_lang("uz")
        bot.send_message(call.message.chat.id, """
Siz o'zbek tilini tanladingiz 🇺🇿
                         
Qaysi mavzuda maqola kerekligini yozing ⬇️ """)
            
    elif call.data == 'English':
        wikipedia.set_lang("en")
        bot.send_message(call.message.chat.id, """
You have selected English 🇺🇸                         

Write on which topic you need an article ⬇️ """)

# Rus tilini ishga tushirish 
@bot.message_handler(func=lambda message: message.text == "🇷🇺 Русский")
def select_language_ru(message):
    wikipedia.set_lang("ru")
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,f"Привет <b>{message.from_user.first_name}👋🏻</b>",parse_mode='HTML',disable_web_page_preview=True, reply_markup=markup)
    bot.send_message(message.chat.id, "Напишите тему статьи: ")

    @bot.message_handler(func=lambda message: True)
    def test_ru(message):
        try:
            inline_markup = InlineKeyboardButton().create_inline_keyboard()
            bot.send_chat_action(message.chat.id, action="typing")
            summary = wikipedia.summary(message.text)
            formatted_message = f"<b>{summary}</b>\n<a href='http://t.me/maqola_search_bot'>@maqola_search_bot</a>"

            bot.send_message(message.chat.id,formatted_message,parse_mode='HTML',disable_web_page_preview=True,reply_markup=inline_markup)
        except:
            bot.send_message(message.chat.id, "Nothing found 😔")

# Uzbek tilini ishga tushirish
@bot.message_handler(func=lambda message: message.text == "🇺🇿 Uzbek")
def select_language_uz(message):
    wikipedia.set_lang("uz")
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,f"Salom <b>{message.from_user.first_name}👋🏻</b>",parse_mode='HTML',disable_web_page_preview=True,reply_markup=markup)
    bot.send_message(message.chat.id, "Qaysi mavzuda maqola kerekligini yozing: ")

    @bot.message_handler(func=lambda message: True)
    def test_uz(message): 
        try:
            inline_markup = InlineKeyboardButton().create_inline_keyboard()
            bot.send_chat_action(message.chat.id, action="typing")
            summary = wikipedia.summary(message.text)
            formatted_message = f"<b>{summary}</b>\n<a href='http://t.me/maqola_search_bot'>@maqola_search_bot</a>"

            bot.send_message(message.chat.id,formatted_message,parse_mode='HTML',disable_web_page_preview=True,reply_markup=inline_markup)
        except:
            bot.send_message(message.chat.id, "Nothing found 😔")
    
# Engliz tilini ishga tushirish 
@bot.message_handler(func=lambda message: message.text == "🇺🇸 English")
def select_language_en(message):
    wikipedia.set_lang("en")
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,f"Hello there <b>{message.from_user.first_name}👋🏻</b>",parse_mode='HTML',disable_web_page_preview=True, reply_markup=markup)
    bot.send_message(message.chat.id, "Write on which topic you need an article: ")

    @bot.message_handler(func=lambda message: True)
    def test_en(message):
        try:
            inline_markup = InlineKeyboardButton().create_inline_keyboard()
            bot.send_chat_action(message.chat.id, action="typing")
            summary = wikipedia.summary(message.text)
            formatted_message = f"<b>{summary}</b>\n<a href='http://t.me/maqola_search_bot'>@maqola_search_bot</a>"

            bot.send_message(message.chat.id,formatted_message,parse_mode='HTML',disable_web_page_preview=True,reply_markup=inline_markup)
        except:
            bot.send_message(message.chat.id, "Nothing found 😔")


if __name__ == "__main__":
    bot.polling(print("Bot ishga tushdi..."))
    
    
