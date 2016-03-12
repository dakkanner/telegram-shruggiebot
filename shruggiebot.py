#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
This bot replies to various /commands in Telegram with emoticon text messages or 
gif video messages.
"""

from telegram import Updater
import logging
import time
import random
from datetime import timedelta, datetime

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Array for (chat ID, datetime of last doorslam)
last_doorslam_time = []

# Array of doorslam gif URLs
doorslam_gifs = [
"http://i.imgur.com/kzXzSRi.gif",
"http://i.imgur.com/ghSiYvp.gif",
"http://i.imgur.com/6eIOZtd.gif",
"http://i.imgur.com/la1uq2g.gif",
"http://i.imgur.com/RxIFFq2.gif",
"http://i.imgur.com/iQTRkrG.gif",
"http://i.imgur.com/wpJBmj2.gif",
"http://i.imgur.com/xmIeU0H.gif",
"http://i.imgur.com/QB6F4Ha.gif",
"http://i.imgur.com/vBcqOlL.gif",
"http://i.imgur.com/qkE3Ucv.gif",
"http://i.imgur.com/jmxD3Uc.gif",
"http://i.imgur.com/Yr9UknU.gif",
"http://i.imgur.com/2kBCdaA.gif",
"http://i.imgur.com/W6piArJ.gif",
"http://i.imgur.com/mn2PFkQ.gif",
"http://i.imgur.com/78pXqSc.gif",
"http://i.imgur.com/htKWL7x.gif",
"http://i.imgur.com/pOOb7Fb.gif",
"http://i.imgur.com/cmRVBdI.gif",
"http://i.imgur.com/IpmFPDn.gif",
"http://i.imgur.com/mkyrCfs.gif",
"http://i.imgur.com/CEZJv7S.gif",
"http://i.imgur.com/bsiBiPI.gif"
]

# Define command handlers here.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='ShruggieBot can shrug.\nUse /shruggie to shrug')


def halp(bot, update):
    halp_text = """
ShruggieBot can shrug. BUT WAIT! THERE'S MORE!

/shruggie - shrug
/sadshruggie - shrug
/lenny - Lenny face
/diretide - GIVE DIRETIDE
/helix - USE HELIX
/ayy - ayy
/flip - flip a table
/unflip - unflip a table
/disapprove - disapproving face
/YEAH _[optional: setup text]_ ; _[optional: punchline text]_ - CSI Miami Simulator 2016
"""
    bot.sendMessage(update.message.chat_id, text=halp_text, parse_mode='Markdown')


def shruggie(bot, update):
    logger.info('Shruggie in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='¯\\_(ツ)_/¯')


def sad_shruggie(bot, update):
    logger.info('Sad shruggie in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='¯\\_(*-_-)_/¯')


def lenny(bot, update):
    logger.info('Lenny in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='( ͡° ͜ʖ ͡°)')


def diretide(bot, update):
    logger.info('Diretide in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='༼ つ ◕_◕ ༽つ GIVE DIRETIDE ༼ つ ◕_◕ ༽つ')


def helix(bot, update):
    logger.info('Helix in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='༼ つ ◕_◕ ༽つ USE HELIX ༼ つ ◕_◕ ༽つ')


def ayy(bot, update):
    logger.info('Ayy in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='(☞ﾟヮﾟ)☞')


def flip(bot, update):
    logger.info('Flip in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='(╯°□°）╯︵ ┻━┻')


def unflip(bot, update):
    logger.info('Unflip in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='┬─┬﻿ ノ( ゜-゜ノ)')


def disapprove(bot, update):
    logger.info('Disapprove in chat %s' % (update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='ಠ_ಠ')


def yeah(bot, update):
    logger.info('Yeah in chat %s' % (update.message.chat_id))
    
    messages = _clean_yeah_message(update.message.text)
    
    message_text = None
    if len(messages) == 0:
        message_text = u"(•_•)\n( •_•)>⌐■-■\n(⌐■_■)\nYEEAAAAAAAH"
    elif len(messages) == 1:
        message_text = u"(•_•)\n( •_•)>⌐■-■\n" + messages[0] + u"\n(⌐■_■)\nYEEAAAAAAAH"
    else:
        message_text = u"(•_•)\n" + messages[0] + u"\n( •_•)>⌐■-■\n" + messages[1] + u"\n(⌐■_■)\nYEEAAAAAAAH"
    
    bot.sendMessage(update.message.chat_id, text=message_text)


def doorslam(bot, update):
    # Only run if doorslam gif hasn't been posted for the last hour in this chat
    # This doesn't really matter so we don't save it to file in case of restarts
    chat_index = None
    for index, item in enumerate(last_doorslam_time):
        if item[0] == update.message.chat_id:
            chat_index = index
            break
    # Add this chat if it wasn't found
    if chat_index is None:
        last_doorslam_time.append((update.message.chat_id, datetime.now() - timedelta(hours=2)))
        chat_index = len(last_doorslam_time) - 1
    
    if datetime.now() > (last_doorslam_time[chat_index][1] + timedelta(hours=1)):
        logger.info('Doorslam in chat %s' % (update.message.chat_id))
        # Wait 10 seconds
        # TODO Implement non-blocking way to wait
        time.sleep(7)
        
        # Get a random doorslam gif
        doorslam_gif = doorslam_gifs[random.randint(0,len(doorslam_gifs) - 1)]
        bot.sendVideo(update.message.chat_id, text='/DOORSLAM', video=doorslam_gif)
        
        # Update time
        last_doorslam_time.pop(chat_index)
        last_doorslam_time.append((update.message.chat_id, datetime.now()))
    else:
        logger.info('Waiting to doorslam in chat %s' % (update.message.chat_id))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


#
# Returns a list of 0, 1, or 2 length with the 
#
def _clean_yeah_message(message):
    cleaned_words_string = message.strip()
    # Split apart the first semicolon into its own word
    cleaned_words_string = cleaned_words_string.replace(';', ' ; ', 1)
    words_list = cleaned_words_string.split(' ')

    cleaned_words = []
    for word in words_list:
        cleaned_words.append(word.strip())
    cleaned_words = list(filter(None, cleaned_words))

    # Remove the /command
    if len (cleaned_words) > 0:
        cleaned_words= cleaned_words[1:]

    logger.info('List of /YEAH words: "%s"' % (','.join(cleaned_words)))
    
    return_array = []
    temp_string = ''
    for word in cleaned_words:
        if len(word) == 1 and word.find(';') > -1:
            if len(temp_string) > 0:
                return_array.append(temp_string)
                temp_string = ''
        else:
            temp_string += word + ' '
    if len(temp_string) > 0:
        return_array.append(temp_string)
        
    return return_array


def main():
    # Create the EventHandler and pass it the bot's token.
    updater = Updater("BOT TOKEN GOES HERE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", start)
    dp.addTelegramCommandHandler("halp", halp)
    dp.addTelegramCommandHandler("shrug", shruggie)
    dp.addTelegramCommandHandler("shruggie", shruggie)
    dp.addTelegramCommandHandler("sadshrug", sad_shruggie)
    dp.addTelegramCommandHandler("sadshruggie", sad_shruggie)
    dp.addTelegramCommandHandler("lenny", lenny)
    dp.addTelegramCommandHandler("diretide", diretide)
    dp.addTelegramCommandHandler("helix", helix)
    dp.addTelegramCommandHandler("ayy", ayy)
    dp.addTelegramCommandHandler("flip", flip)
    dp.addTelegramCommandHandler("unflip", unflip)
    dp.addTelegramCommandHandler("disapprove", disapprove)
    dp.addTelegramCommandHandler("yeah", yeah)
    dp.addTelegramCommandHandler("YEAH", yeah)
    dp.addTelegramCommandHandler("DOORSLAM", doorslam)

    # Log all errors
    dp.addErrorHandler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until the you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
