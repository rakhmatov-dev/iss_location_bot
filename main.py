import telebot
import pandas as pd
from templates import *
import requests

ROOT_FOLDER = 'C:/Users/raxx/PycharmProjects/iss_location_bot/'
API_KEY = 'YOUR TOKEN'
bot = telebot.TeleBot(API_KEY)

def save_chat_id(chat_id, latitude=0.0, longitude=0.0):
    try:
        df_chats = pd.read_csv(f"{ROOT_FOLDER}/resources/chats.csv")
        if not df_chats.isin([chat_id]).any().any():
            df_append = pd.DataFrame({
                    'id': [chat_id],
                    'lat': [latitude],
                    'lng': [longitude]
                })
            df_chats = pd.concat([df_chats, df_append], ignore_index=True, axis=0)
            if 'Unnamed: 0' in df_chats:
                df_chats.drop(columns=['Unnamed: 0'], inplace=True)
            df_chats.reset_index(drop=True, inplace=True)
            df_chats.to_csv(f"{ROOT_FOLDER}/resources/chats.csv")

    except FileNotFoundError:
        df_chat = pd.DataFrame({
            'id': [chat_id],
            'lat': [latitude],
            'lng': [longitude]
        })
        df_chat.to_csv(f"{ROOT_FOLDER}/resources/chats.csv")


def get_current_location_of_iss():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    if response.status_code == 200:
        data = response.json()
        longitude = data['iss_position']['longitude']
        latitude = data['iss_position']['latitude']
        return latitude, longitude
    else:
        return 0, 0


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        chat_id = message.chat.id

        # Saving chat id to csv file
        save_chat_id(chat_id)
        #

        # Sending greetings message to new user
        first_name = message.from_user.first_name
        # response_text = MESSAGE_GREETINGS.replace('#, first_name#', f" {first_name}" if len(first_name) > 0 else '')
        response_text = MESSAGE_GREETINGS.format(f", {first_name}" if len(first_name) > 0 else '')
        bot.send_message(message.chat.id, response_text)
        #


@bot.message_handler(commands=['help'])
def start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, MESSAGE_LIST_OF_COMMANDS)


@bot.message_handler(commands=['where_is_iss'])
def where_is_iss(message):
    if message.chat.type == 'private':
        latitude, longitude = get_current_location_of_iss()
        bot.send_location(message.chat.id, latitude, longitude)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    F = 2
    if message.chat.type == 'private':
        latitude,  longitude = message.location.latitude, message.location.longitude
        # print(latitude)
        # print(longitude)


@bot.message_handler(func=lambda m: True) # lambda ???
def handle_all_messages(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, MESSAGE_REPLY_FOR_ALL_OTHER_MESSAGES)
        bot.send_message(message.chat.id, MESSAGE_LIST_OF_COMMANDS)

bot.infinity_polling()
