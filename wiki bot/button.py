import telebot

class InlineKeyboardButton:
    @staticmethod
    def create_inline_keyboard():
        inline_markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton("🇷🇺", callback_data='Русский')
        btn2 = telebot.types.InlineKeyboardButton("🇺🇿", callback_data='Uzbek')
        btn3 = telebot.types.InlineKeyboardButton("🇺🇸", callback_data='English')
        inline_markup.add(btn1, btn2, btn3)
        return inline_markup
    
class KeyboardButton:
    @staticmethod
    def create_button_keyboard():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("🇷🇺 Русский")
        btn2 = telebot.types.KeyboardButton('🇺🇿 Uzbek')
        btn3 = telebot.types.KeyboardButton("🇺🇸 English")
        markup.add(btn1, btn2, btn3)
        return markup