import telebot, config, sqlite3, logging, asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
file_handler = logging.FileHandler('logs\log.log', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
 
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Bot has been laucnhed.')

API_TOKEN = config.TG_BOT_TOKEN

bot = AsyncTeleBot(API_TOKEN)

markup = types.InlineKeyboardMarkup(row_width=5)

btn_0 = types.InlineKeyboardButton('0', callback_data='0')
btn_1 = types.InlineKeyboardButton('1', callback_data='1')
btn_2 = types.InlineKeyboardButton('2', callback_data='2')
btn_3 = types.InlineKeyboardButton('3', callback_data='3')
btn_4 = types.InlineKeyboardButton('4', callback_data='4')
btn_5 = types.InlineKeyboardButton('5', callback_data='5')
btn_6 = types.InlineKeyboardButton('6', callback_data='6')
btn_7 = types.InlineKeyboardButton('7', callback_data='7')
btn_8 = types.InlineKeyboardButton('8', callback_data='8')
btn_9 = types.InlineKeyboardButton('9', callback_data='9')
btn_point = types.InlineKeyboardButton('.', callback_data='.')

btn_blank = types.InlineKeyboardButton(' ', callback_data='nothing')
btn_clear = types.InlineKeyboardButton('C', callback_data='clear')
btn_delete = types.InlineKeyboardButton('<=', callback_data='delete')
btn_equal = types.InlineKeyboardButton('=', callback_data='equal')
btn_divide = types.InlineKeyboardButton('/', callback_data='/')
btn_mult = types.InlineKeyboardButton('*', callback_data='*')
btn_minus = types.InlineKeyboardButton('-', callback_data='-')
btn_plus = types.InlineKeyboardButton('+', callback_data='+')
btn_bracket_left = types.InlineKeyboardButton('(', callback_data='(')
btn_bracket_right = types.InlineKeyboardButton(')', callback_data=')')
btn_sqr = types.InlineKeyboardButton('^', callback_data='**')
btn_sqrt = types.InlineKeyboardButton('\U0000221Ax', callback_data='sqrt')

markup.add(btn_clear, btn_delete, btn_bracket_left, btn_bracket_right, btn_divide,
           btn_sqrt, btn_7, btn_8, btn_9, btn_mult,
           btn_sqr, btn_4, btn_5, btn_6, btn_minus,
           btn_blank, btn_1, btn_2, btn_3, btn_plus,
           btn_blank, btn_blank, btn_0, btn_point, btn_equal)


def write_db(chat_id, value):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    chat_id INTEGER PRIMARY KEY,
    value TEXT
    )
    ''')   

    cursor.execute('REPLACE INTO Users (chat_id, value) VALUES(?, ?)', (chat_id, value))
    
    connection.commit()
    connection.close()

def read_db(chat_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT value FROM Users WHERE chat_id == ?', (chat_id,))
    value = cursor.fetchone()[0]
    
    connection.commit()
    connection.close()
    
    return value
    

@bot.message_handler(commands=['help', 'start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Чтобы воспользоваться калькулятором, пропиши команду /calclater')


@bot.message_handler(commands=['calclater'])
async def calclater(message):
    await bot.send_message(message.chat.id, '0', reply_markup=markup)
    write_db(message.chat.id, '')

@bot.callback_query_handler(func=lambda call:True)
async def calclater(call):
    
    value = read_db(call.message.chat.id)
    
    data = call.data
    old_value = value
    
    if data == 'equal':
        try:
            value = str(eval(value))
            write_db(call.message.chat.id, value)
            
        except ZeroDivisionError:
            value = ''
            write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='ERROR: Деление на ноль', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Division by zero] - [value: {value}]")
        except SyntaxError:
            value = ''
            write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='ERROR: Неправильный синтаксис', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Invalid syntax] - [value: {value}]")
        except ValueError:
            value = ''
            write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='ERROR: Ошибка значения', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Value Error] - [value: {value}]")
      
    elif data == 'clear':
        value = ''
        write_db(call.message.chat.id, value)
    elif data == 'delete':
        try:
            value = value[:-1]
            write_db(call.message.chat.id, value)
        except:
            pass
    elif data == 'sqrt':
        value = str(float(value)**0.5)
        write_db(call.message.chat.id, value)
    elif data == 'nothing':
        pass
    else:
        value += data
        write_db(call.message.chat.id, value)
        
    await bot.answer_callback_query(call.id)
        
    if value != old_value: 
        if value == '':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='0', reply_markup=markup)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=value, reply_markup=markup)
    
    logger.info(f"[chat_id: {call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name,}] - [value: {value}]")
    

asyncio.run(bot.polling())

# todo: value для каждого пользователя по chat_id через БД SQLite | СДЕЛАНО!
# todo: добавить логирование | СДЕЛАНО!
# todo: добавить скобочки и проверить работают ли они с eval() + сделал кнопки sqrt и sqr | СДЕЛАНО!
# todo: сделать бота асинхронным | СДЕЛАНО!
# todo: переписать бота на библиотеке aiogramm