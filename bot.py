import config
import asyncio, logging, sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


async def write_db(chat_id, value):
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

async def read_db(chat_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT value FROM Users WHERE chat_id == ?', (chat_id,))
    value = cursor.fetchone()[0]
    
    connection.commit()
    connection.close()
    
    return value


logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
file_handler = logging.FileHandler('logs\log.log', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
 
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Bot has been laucnhed.')


bot = Bot(config.TG_BOT_TOKEN)

dp = Dispatcher()

btn_0 = types.InlineKeyboardButton(text='0', callback_data='0')
btn_1 = types.InlineKeyboardButton(text='1', callback_data='1')
btn_2 = types.InlineKeyboardButton(text='2', callback_data='2')
btn_3 = types.InlineKeyboardButton(text='3', callback_data='3')
btn_4 = types.InlineKeyboardButton(text='4', callback_data='4')
btn_5 = types.InlineKeyboardButton(text='5', callback_data='5')
btn_6 = types.InlineKeyboardButton(text='6', callback_data='6')
btn_7 = types.InlineKeyboardButton(text='7', callback_data='7')
btn_8 = types.InlineKeyboardButton(text='8', callback_data='8')
btn_9 = types.InlineKeyboardButton(text='9', callback_data='9')
btn_point = types.InlineKeyboardButton(text='.', callback_data='.')

btn_blank = types.InlineKeyboardButton(text=' ', callback_data='nothing')
btn_clear = types.InlineKeyboardButton(text='C', callback_data='clear')
btn_delete = types.InlineKeyboardButton(text='<=', callback_data='delete')
btn_equal = types.InlineKeyboardButton(text='=', callback_data='equal')
btn_divide = types.InlineKeyboardButton(text='/', callback_data='/')
btn_mult = types.InlineKeyboardButton(text='*', callback_data='*')
btn_minus = types.InlineKeyboardButton(text='-', callback_data='-')
btn_plus = types.InlineKeyboardButton(text='+', callback_data='+')
btn_bracket_left = types.InlineKeyboardButton(text='(', callback_data='(')
btn_bracket_right = types.InlineKeyboardButton(text=')', callback_data=')')
btn_sqr = types.InlineKeyboardButton(text='^', callback_data='**')
btn_sqrt = types.InlineKeyboardButton(text='\U0000221Ax', callback_data='sqrt')

markup = types.InlineKeyboardMarkup(inline_keyboard=[
    [btn_clear, btn_delete, btn_bracket_left, btn_bracket_right, btn_divide],
    [btn_sqrt, btn_7, btn_8, btn_9, btn_mult],
    [btn_sqr, btn_4, btn_5, btn_6, btn_minus],
    [btn_blank, btn_1, btn_2, btn_3, btn_plus],
    [btn_blank, btn_blank, btn_0, btn_point, btn_equal]
    ])


@dp.message(Command('start', 'help'))
async def cmd_start(message: types.Message):
    await message.answer('Чтобы воспользоваться калькулятором, пропиши команду /calclater')

@dp.message(Command('calclater'))
async def cmd_calclater(message: types.Message):
    await message.answer('0', reply_markup=markup)
    await write_db(message.chat.id, '')

@dp.callback_query(lambda call: True) 
async def calclater_query(call: types.CallbackQuery): 
  
    value = await read_db(call.message.chat.id)
    
    data = call.data
    old_value = value
    
    if data == 'equal':
        try:
            value = str(eval(value))
            await write_db(call.message.chat.id, value)
            
        except ZeroDivisionError:
            value = ''
            await write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='ERROR: Деление на ноль', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Division by zero] - [value: {value}]")
        except SyntaxError:
            value = ''
            await write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='ERROR: Неправильный синтаксис', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Invalid syntax] - [value: {value}]")
        except ValueError:
            value = ''
            await write_db(call.message.chat.id, value)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='ERROR: Ошибка значения', reply_markup=markup)
            logger.error(f"[chat_id: {call.message.chat.id}] - [ERROR: Value Error] - [value: {value}]")
      
    elif data == 'clear':
        value = ''
        await write_db(call.message.chat.id, value)
    elif data == 'delete':
        try:
            value = value[:-1]
            await write_db(call.message.chat.id, value)
        except:
            pass
    elif data == 'sqrt':
        value = str(float(value)**0.5)
        await write_db(call.message.chat.id, value)
    elif data == 'nothing':
        pass
    else:
        value += data
        await write_db(call.message.chat.id, value)
        
    await bot.answer_callback_query(call.id)
        
    if value != old_value: 
        if value == '':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='0', reply_markup=markup)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=value, reply_markup=markup)
    
    logger.info(f"[chat_id: {call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name,}] - [value: {value}]")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

# todo: value для каждого пользователя по chat_id через БД SQLite | СДЕЛАНО!
# todo: добавить логирование | СДЕЛАНО!
# todo: добавить скобочки и проверить работают ли они с eval() + сделал кнопки sqrt и sqr | СДЕЛАНО!
# todo: сделать бота асинхронным | СДЕЛАНО!
# todo: переписать бота на библиотеке aiogram | СДЕЛАНО!
# todo: разобраться с БД, скорее всего из-за неё тормозит | СДЕЛАНО!