import telebot
import requests
import mysql.connector

"""
database config
"""
db_name='testGeo'
user='root'
password='1234'
host='localhost'
try:
	connect = mysql.connector.connect(host=host,database=db_name,user=user, password=password)
except mysql.connector.Error as e:
	print(e)

params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)



bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "/corona_ru - oficial statistic of COVID-19 in Russia")


@bot.message_handler(commands=['corona_ru', 'coronavirus_ru'])
def corona(message):
	resp = requests.get(url='https://coronavirus-tracker-api.herokuapp.com/v2/locations', params=params)
	data = resp.json()
	mes = r"Население {0} /n Заболевших {1} /n  Умерших {2}".format(data['locations'][187]['country_population'], data['locations'][187]['latest']['confirmed'],data['locations'][187]['latest']['deaths'], parse_mode='Markdown')
	bot.reply_to(message, mes)

@bot.message_handler(content_types=['text'])
def send_text(message:telebot.types.Message):
	if message.text.lower() == 'привет':

		bot.send_message(message.chat.id, 'Привет, {0}'.format( str(message.from_user.first_name)))

	if message.text.lower() == 'где':
		location=''
		cursor = connect.cursor()
		cursor.execute("SELECT longtitude, latitude FROM Log LIMIT 1")
		row = cursor.fetchone()
		while row is not None:
			location = cursor.fetchone()

		bot.send_message(message.chat.id, 'Где-то в  {0}'.format(location))




bot.polling()