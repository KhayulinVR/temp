import re
from time import process_time
from fractions import Fraction
from traceback import print_tb
import pandas as pd
import math
from traceback import print_tb
from pandas import wide_to_long
import telebot
import random as r

# define
debug = True


def delete_inf(temp_str):
    new_str = ""
    i = 0
    while i < len(temp_str):
        if temp_str[i] != " ":
            new_str += temp_str[i]
        if temp_str[i] == "\n":
            i+=1
        i+=1
    return new_str


def transfer_lst_to_str(lst_num, lst_operation, lst_det):
    # lst_num  - список счислителями
    # lst_oper - список с мат операторами
    # lst_det  - список с знам
    count_oper = 0
    count_nummer = 0
    all_num_str = " "
    all_oper_str = " "
    all_det_str = " "
    flag = True
    for i in range(len(lst_num)+len(lst_operation)):
        if flag:
            width = max(len(str(lst_num[count_nummer])), len(str(lst_det[count_nummer])))  # 1
            num_str = " " * math.ceil((width - len(str(lst_num[count_nummer]))) / 2) + str(lst_num[count_nummer]) + " " * (
                    (width - len(str(lst_num[count_nummer]))) // 2)  # 1
            det_str = " " * math.ceil((width - len(str(lst_det[count_nummer]))) / 2) + str(lst_det[count_nummer]) + " " * (
                    (width - len(str(lst_det[count_nummer]))) // 2)  # 1
            count_nummer += 1
            all_oper_str += width*"-" #1
        else:
            all_oper_str += " " + lst_operation[count_oper] + " "
            count_oper+=1
            all_num_str += 3*" "
            all_det_str += 3*" " #!!!!!
        flag = not flag
        all_num_str += num_str#1
        all_det_str += det_str#1
        num_str = ""
        det_str = ""
    all_sent = all_num_str + "\n" + all_oper_str + "\n" + all_det_str
    return all_sent


def trasfer_scvText_to_tgText(str_ex):
    lst_str = str_ex.split("\n")

    for i in range(1, len(lst_str)):
        lst_str[i] = lst_str[i][1:]
    lst_fraction_temp = []
    for i in range(len(lst_str)):
        lst_temp = []
        str_temp = ""
        for j in range(len(lst_str[i])):
            if (lst_str[i][j] != " ") or lst_str[i][j] != " ":
                str_temp += lst_str[i][j]
            else:
                if str_temp != "":
                    try:
                        lst_temp.append(int(str_temp))
                    except:
                        if str_temp == "+" or str_temp == "-" or str_temp == "*" or str_temp == "/":
                            lst_temp.append(str_temp)
                    str_temp = ""
        if str_temp != "":
            try:
                lst_temp.append(int(str_temp))
            except:
                if str_temp == "+" or str_temp == "-" or str_temp == "*" or str_temp == "/":
                    lst_temp.append(str_temp)

        lst_fraction_temp.append(lst_temp)

    return transfer_lst_to_str(lst_fraction_temp[0], lst_fraction_temp[1], lst_fraction_temp[2])

# ===========================
# бд тест
def take_data_from_db_csv_with_tab_to_str(name_db, num_column, num_line):
    df_orders = pd.read_csv(name_db, delimiter='\t')

    if len(df_orders.columns) > num_column:
        column = df_orders.iloc[:, num_column]
        return column[num_line]

# ===========================
# бот
bot = telebot.TeleBot(token_token)

def add_quotes(temp_str):
    return '```'+temp_str+'```'

def transfet_example_with_slash_to_tgText(temp_str):
    temp_lst = re.split(r'([+-])', temp_str)
    # Выводим результат
    # print(temp_lst)
    lst_num = []
    lst_oper = []
    lst_det = []
    for i in temp_lst:
        if i == '+' or i == '-':
            lst_oper.append(i)
        else:
            lst_num.append(int(i.split("/")[0]))
            lst_det.append(int(i.split("/")[1]))
    return transfer_lst_to_str(lst_num, lst_oper, lst_det)

# print(transfet_example_with_slash_to_tgText("9/8+999999/8-8/9999999999+7/987654"))

def generate_random_example():
    temp_str = ""
    lst_oper = ['+', '-']
    for i in range(r.randint(2, 4)):
        temp_str += r.choice(lst_oper)
        temp_str += str(r.randint(1, 10000))
        temp_str += '/'
        temp_str += str(r.randint(1, 10000))
    return temp_str[1:]



@bot.message_handler(commands=['start', '1', '2', '3', '4', '5', '6', 'generate'])
def send_welcome(message):
    if message.text == '/generate':
        bot.send_message(message.from_user.id,
                         add_quotes(
                             (transfet_example_with_slash_to_tgText(generate_random_example()))),
                         parse_mode='MarkdownV2'
                         )
    elif message.text == '/start':
        bot.send_message(message.from_user.id, f""" твой id {message.from_user.id}""")
        bot.send_message(message.from_user.id, f""" message это {message}""")
    elif 1 <= int(message.text[1:]) <= 7:
        # print("+++++++++++++++++")
        # print(transfet_example_with_slash_to_tgText(take_data_from_db_csv_with_tab_to_str('test2.csv', 6, int(message.text[1:]))))
        # print("+++++++++++++++++")


        bot.send_message(message.from_user.id,
                         add_quotes(
                             (transfet_example_with_slash_to_tgText(
                                 take_data_from_db_csv_with_tab_to_str(
                                     'test2.csv',
                                     6, int(message.text[1:]))))),
                         parse_mode='MarkdownV2'
                         )

    elif message.text == '/try':
        g = 5 / 0


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.from_user.id, 'Введи мне команду')
    # bot.send_message(message.from_user.id, "```"+trasfer_scvText_to_tgText(str_ex)+"```", parse_mode='MarkdownV2')

bot.infinity_polling()
