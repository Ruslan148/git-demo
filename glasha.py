# -*- coding: utf-8 -*-

import telebot
bot = telebot.TeleBot("1039007003:AAHhmrQOhH081DoKXOI_HDoOrSiGhy3-6w8")
import bot_dict
import random
import re
import time

def has_word_in_message(words, message):
    for word in words:
        if (word in message):
            return True
    return False

def log(message):
    name = message.from_user.username if message.from_user.username != None else message.from_user.first_name
    print('log: ' + str(name) + ': in "' + str(message.chat.title) + '": "' + str(message.text) + '" at ' + str(time.ctime(int(message.date))))

def logAnswer(name, answer):
    print('answer: ' + '[' + name + '] ' + answer)

@bot.message_handler(content_types=["text"])
def response(message):
    message_text = message.text.lower()
    if ('ping' in message_text):
        log(message)
        return bot.send_message(message.chat.id, 'pong')

    nameIncluded = has_word_in_message(bot_dict.names, message_text)
    if (not nameIncluded): return
    log(message)

    mentionInMessage = re.findall(r'@[\w]+', message_text)

    dictionary = bot_dict.dictionary
    random.shuffle(dictionary)
    for dictionary in dictionary:
        keywordIncluded = has_word_in_message(dictionary['keys'], message_text)
        if (not keywordIncluded): continue

        if (len(mentionInMessage) > 0):
            answer = mentionInMessage[0] + ' ' + random.choice(dictionary['answers'])
        else:
            answer = random.choice(dictionary['answers'])
        logAnswer(dictionary['name'], answer)
        return bot.send_message(message.chat.id, answer)

    answer = random.choice(bot_dict.fallback)
    logAnswer('fallback', answer)
    return bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.polling(none_stop=True)
