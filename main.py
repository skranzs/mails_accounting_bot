from imports import *
from class_remember import remember
from insert_letter import insert_letter
from actual_date import get_date
from save_pdf import generate_pdf_by_type

@bot.message_handler(commands=['start'])
def handle_start(message, edit_flag=False):
    remember.reset()
    markup = InlineKeyboardMarkup()
    if message.chat.id in roles:
        current_role = roles[message.chat.id]
        btn1 = InlineKeyboardButton('Присвоить номер письма', callback_data='assign_number')
        btn2 = InlineKeyboardButton('Сменить статус письма', callback_data='003')
        btn3 = InlineKeyboardButton('Выгрузить pdf', callback_data='pdf')
        btn4 = InlineKeyboardButton('⚙️ Настройки', callback_data='008')
        btn5 = InlineKeyboardButton('Удалить письмо', callback_data='023')
        if current_role == 'ГИП':
            markup.add(btn1, btn5)
            markup.add(btn3)
        if current_role == 'Секретарь':
            markup.add(btn1, btn2)
        if current_role == 'Админ':
            markup.add(btn1, btn2)
            markup.add(btn3, btn5)
            markup.add(btn4)
        if current_role == 'Инженер':
            markup.add(btn3)
        if not edit_flag:
            bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите действие', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'У Вас нет роли. Напишите администратору для получения.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if strw(call, 'assign_number'):
        print(call.data, 'CALL DATA')
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Да', callback_data='yes')
        btn2 = InlineKeyboardButton('Нет', callback_data='no')
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Письмо исходящее?', reply_markup=markup)
    if strw(call, 'yes'):
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Кому адресовано письмо?(наименование контрагента)')
        bot.register_next_step_handler(msg, register_name_contragent)
    if strw(call, 'no'):
        remember.set_from_us(False)
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='От кого адресовано письмо?(наименование контрагента)')
        bot.register_next_step_handler(msg, register_name_contragent)
    if strw(call, '001'):
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите номер договора')
        bot.register_next_step_handler(msg, register_contract_id)
    if strw(call, '002'):
        remember.set_contract_id('-')
        topic_of_letter(call.message, edit_flag=True)
    if strw(call, 'pdf'):
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Входящие', callback_data='006')
        btn2 = InlineKeyboardButton('Исходящие', callback_data='007')
        keyboard.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите тип писем', reply_markup=keyboard)
    if strw(call, '006') or strw(call, '007'):
        type_letter = 'Вх'
        if strw(call, '007'):
            type_letter = 'Исх'
        pdf_path = f'{type_letter}.pdf'
        generate_pdf_by_type('letters.db', pdf_path, type_letter)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with open(pdf_path, 'rb') as pdf:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Вернуться в меню', callback_data='doc_menu'))
            bot.send_document(call.message.chat.id, pdf, reply_markup=keyboard)
    if strw(call, 'menu'):
        handle_start(call.message, edit_flag=True)
    if strw(call, 'doc_menu'):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        handle_start(call.message)
    if strw(call, '003'):
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Исходящее', callback_data='004')
        btn2 = InlineKeyboardButton('Входящее', callback_data='005')
        btn3 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите тип письма:', reply_markup=markup)
    if strw(call, '004') or strw(call, '005'):
        if strw(call, '004'):
            remember.set_type('Исх')
        else:
            remember.set_type('Вх')
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите номер письма:')
        bot.register_next_step_handler(msg, register_number)
    if strw(call, '008'):
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Изменить роль', callback_data='009')
        btn2 = InlineKeyboardButton('Удалить сотрудника', callback_data='010')
        btn3 = InlineKeyboardButton('Добавить сотрудника', callback_data='011')
        markup.add(btn1)
        markup.add(btn2, btn3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите действие:', reply_markup=markup)
    if strw(call, '011'):
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите TG ID нового сотрудника\n\nПолучить его можно в боте @getmyid_bot, новому юзеру достаточно написать туда любое сообщение.')
        bot.register_next_step_handler(msg, register_name_user)
    if strw(call, '009'):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id, fullname FROM users")
        rows = cursor.fetchall()
        conn.close()

        markup = InlineKeyboardMarkup(row_width=1)
        for telegram_id, fullname in rows:
            button = InlineKeyboardButton(
                text=fullname,
                callback_data=f'012|{str(telegram_id)}'
            )
            if telegram_id != call.message.chat.id:
                markup.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите сотрудника:', reply_markup=markup)
    if strw(call, '012'):
        tg_id = splc(call)
        markup = InlineKeyboardMarkup()
        current_role = roles[int(tg_id)]
        btn1 = InlineKeyboardButton('ГИП', callback_data=f'013|{tg_id}')
        btn2 = InlineKeyboardButton('Секретарь', callback_data=f'014|{tg_id}')
        btn3 = InlineKeyboardButton('Админ', callback_data=f'015|{tg_id}')
        btn4 = InlineKeyboardButton('Инженер', callback_data=f'016|{tg_id}')
        if current_role != 'ГИП':
            markup.add(btn1)
        if current_role != 'Секретарь':
            markup.add(btn2)
        if current_role != 'Админ':
            markup.add(btn3)
        if current_role != 'Инженер':
            markup.add(btn4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите роль:', reply_markup=markup)
    if strw(call, '013') or strw(call, '014') or strw(call, '015') or strw(call, '016'):
        new_role = 'ГИП'
        if strw(call, '014'):
            new_role = 'Секретарь'
        if strw(call, '015'):
            new_role = 'Админ'
        if strw(call, '016'):
            new_role = 'Инженер'
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users
            SET role = ?
            WHERE telegram_id = ?
        """, (new_role, splc(call)))
        conn.commit()
        conn.close()
        roles[int(splc(call))] = new_role
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Вернуться в меню', callback_data=f'menu')
        markup.add(btn1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы успешно изменили роль!', reply_markup=markup)
    if strw(call, '010'):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id, fullname FROM users")
        rows = cursor.fetchall()
        conn.close()

        markup = InlineKeyboardMarkup(row_width=1)
        for telegram_id, fullname in rows:
            button = InlineKeyboardButton(
                text=fullname,
                callback_data=f'017|{str(telegram_id)}'
            )
            if telegram_id != call.message.chat.id:
                markup.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите сотрудника:', reply_markup=markup)
    if strw(call, '017'):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname FROM users WHERE telegram_id = ?", (splc(call),))
        rows = cursor.fetchall()
        conn.close()
        name = str(rows[0])[2:-3]
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Да, подтверждаю', callback_data=f'018|{splc(call)}')
        btn2 = InlineKeyboardButton('Нет, вернуться в меню', callback_data='menu')
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы точно хотите удалить сотрудника {name}?', reply_markup=markup)
    if strw(call, '018'):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE telegram_id = ?", (splc(call),))
        conn.commit()
        conn.close()
        del roles[int(splc(call))]
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы успешно удалили сотрудника.', reply_markup=markup)
    if strw(call, '019') or strw(call, '020') or strw(call, '021') or strw(call, '022'):
        new_role = 'ГИП'
        if strw(call, '020'):
            new_role = 'Секретарь'
        if strw(call, '021'):
            new_role = 'Админ'
        if strw(call, '022'):
            new_role = 'Инженер'
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        fullname, telegram_id = remember.get_user()
        cursor.execute("""
        INSERT INTO users (telegram_id, username, role, fullname)
        VALUES (?, ?, ?, ?)
    """, (telegram_id, '', new_role, fullname))
        conn.commit()
        conn.close()
        roles[int(splc(call))] = new_role
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Вернуться в меню', callback_data=f'menu')
        markup.add(btn1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы успешно добавили сотрудника!', reply_markup=markup)
    if strw(call, '023'):
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Исходящее', callback_data='024')
        btn2 = InlineKeyboardButton('Входящее', callback_data='025')
        btn3 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите тип письма:', reply_markup=markup)
    if strw(call, '024') or strw(call, '025'):
        if strw(call, '024'):
            remember.set_type('Исх')
        else:
            remember.set_type('Вх')
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите номер письма согласно журналу выбранного типа:')
        bot.register_next_step_handler(msg, register_number_delete_letter)
    if strw(call, '026'):
        conn = sqlite3.connect("letters.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM outgoing_letters WHERE type_id = ? AND type = ?", (splc(call), remember.get_type()))
        conn.commit()
        conn.close()
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        keyboard.add(btn1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы успешно удалили письмо.', reply_markup=keyboard)
        


def register_number_delete_letter(message):
    conn = sqlite3.connect("letters.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM outgoing_letters
        WHERE type = ? AND type_id = ?
    """, (remember.get_type(), message.text))
    result = cursor.fetchone()
    conn.close()
    print(result)
    if result:
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Подтверждаю', callback_data=f'026|{message.text}')
        btn2 = InlineKeyboardButton('Нет, вернуться в меню', callback_data='menu')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, f'Вы подтверждаете удаление? Содержание письма: {result[-4]} {result[-2]} {result[-3]}', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Попробовать ещё раз', callback_data='003')
        btn2 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        keyboard.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, 'Письмо не найдено', reply_markup=keyboard)


def register_name_user(message):
    msg = bot.send_message(message.chat.id, 'Введите имя сотрудника') 
    bot.register_next_step_handler(msg, choose_role_for_new_user, message.text)


def choose_role_for_new_user(message, tg_id):
    name = message.text
    remember.set_user(name, tg_id)
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('ГИП', callback_data=f'019|{tg_id}')
    btn2 = InlineKeyboardButton('Секретарь', callback_data=f'020|{tg_id}')
    btn3 = InlineKeyboardButton('Админ', callback_data=f'021|{tg_id}')
    btn4 = InlineKeyboardButton('Инженер', callback_data=f'022|{tg_id}')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=markup)



def register_number(message):
    conn = sqlite3.connect("letters.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM outgoing_letters
        WHERE type = ? AND type_id = ?
    """, (remember.get_type(), message.text))
    result = cursor.fetchone()
    conn.close()
    if result:
        msg = bot.send_message(message.chat.id, 'Введите новый статус:')
        bot.register_next_step_handler(msg, register_new_status, message.text)
    else:
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Попробовать ещё раз', callback_data='003')
        btn2 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        keyboard.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, 'Письмо не найдено', reply_markup=keyboard)



def register_new_status(message, number):
    new_status = message.text
    conn = sqlite3.connect("letters.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE outgoing_letters
        SET status = ?
        WHERE type = ? AND id = ?
    """, (new_status, remember.get_type(), number))

    conn.commit()
    conn.close()
    updated_rows = cursor.rowcount
    if updated_rows:
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Заполнить ещё раз', callback_data='003')
        btn2 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы успешно изменили статус', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Попробовать ещё раз', callback_data='003')
        btn2 = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Произошла ошибка, свяжитесь с администратором', reply_markup=keyboard)


def register_name_contragent(message):
    name_contragent = message.text
    remember.set_name_cntragnt(name_contragent)
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Да', callback_data='001')
    btn2 = InlineKeyboardButton('Нет', callback_data='002')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Письмо в рамках заключенного договора?', reply_markup=markup)

def register_contract_id(message):
    contract_id = ''.join(message.text.split('-')[0])
    remember.set_contract_id(contract_id)
    topic_of_letter(message)
    

def topic_of_letter(message, edit_flag=False, msg=None):
    if not edit_flag:
        msg = bot.send_message(message.chat.id, 'Введите тему письма')
    else:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Введите тему письма')
    bot.register_next_step_handler(msg, register_topic_of_letter)
    

def register_topic_of_letter(message):
    topic = message.text
    remember.set_topic(topic)
    msg = bot.send_message(message.chat.id, 'Введите ФИО исполнителя, должность')
    bot.register_next_step_handler(msg, register_fio)

def register_fio(message):
    fio = message.text
    remember.set_FIO(fio)
    date, time = get_date()
    contract, name_cntragnt, FIO,  topic = remember.get_contract_id(), remember.get_name_cntragnt(), remember.get_FIO(), remember.get_topic()
    s, s1, type_of_letter = 'исходящего', 'исходящих', 'Исх'
    if remember.get_from_us() == False:
        s, s1, type_of_letter = 'входящего', 'входящих', 'Вх'
    print(type_of_letter, 'HERe')
    id_letter = insert_letter(contract, 1, date, time, name_cntragnt, FIO, topic, 'ожидание', type_of_letter)
    remember.reset()
    conn = sqlite3.connect('letters.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM outgoing_letters
        WHERE contract_number=? AND date=? AND time=?
          AND contractor=? AND FIO=? AND subject=?
        ORDER BY id DESC
        LIMIT 1
    """, (contract, date, time, name_cntragnt, FIO, topic))
    
    result = cursor.fetchone()
    conn.close()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Вернуться в меню', callback_data='menu'))
    bot.send_message(message.chat.id, f'Номер {s} письма: {result[0]}\nНомер договора: {contract} / Номер письма согласно журнала {s1} писем: {id_letter}', reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(non_stop=True)
