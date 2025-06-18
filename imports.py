from telebot.types import *
import telebot as tb
import sqlite3
bot = tb.TeleBot('7320766736:AAFK0Qc7k2mwtspoxGTv_kpeX-tsQufvZKQ')


def strw(call, znach):
    if call.data.startswith(f'{znach}'):
        return True
    else:
        return False


def splc(call):
    return call.data.split('|')[1]



conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("SELECT telegram_id, role FROM users")
rows = cursor.fetchall()
conn.close()

roles = {telegram_id: role for telegram_id, role in rows}