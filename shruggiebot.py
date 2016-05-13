#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
This bot replies to various /commands in Telegram with emoticon text messages or 
gif video messages.
"""

from telegram.ext import Updater, CommandHandler
import logging
import time
import random
import thread
from datetime import timedelta, datetime

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Array for (chat ID, datetime of last doorslam)
last_doorslam_time = []

# Array for (chat ID, user ID, datetime of last high five)
last_high_five_time = []

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

# Array of normal high five gif URLs
normal_high_five_gifs = [
"https://i.imgur.com/UCZ4X8v.gif",
"https://i.imgur.com/LeWppmm.gif",
"https://i.imgur.com/I0LC7R7.gif",
"https://i.imgur.com/cARCCNV.gif",
"https://i.imgur.com/Ka9fndL.gif",
"https://i.imgur.com/91xmP3h.gif",
"https://i.imgur.com/RbQefRY.gif",
"https://i.imgur.com/SUqtHOu.gif",
"https://i.imgur.com/OBVGeK5.gif",
"https://i.imgur.com/WQOyz1B.gif",
"https://i.imgur.com/GR2zwdx.gif",
"https://i.imgur.com/6cxZvXc.gif",
"https://i.imgur.com/Oagx0v2.gif",
"https://i.imgur.com/KJyn9vk.gif",
"https://i.imgur.com/lNrFb0n.gif",
"https://i.imgur.com/UgCcB4T.gif",
"https://i.imgur.com/3g6VJBI.gif",
"https://i.imgur.com/RJS1SeF.gif",
"https://i.imgur.com/rf7N1Ly.gif",
"https://i.imgur.com/ttHFqE4.gif",
"https://i.imgur.com/FZYtCeU.gif",
"https://i.imgur.com/7uBYgBo.gif",
"https://i.imgur.com/MdDuvt5.gif",
"https://i.imgur.com/qVCdKpX.gif",
"https://i.imgur.com/umnRyMn.gif",
"https://i.imgur.com/CatI03o.gif",
"https://i.imgur.com/U0cvYCZ.gif",
"https://i.imgur.com/6EMy1Nc.gif",
"https://i.imgur.com/O6q4Wig.gif",
"https://i.imgur.com/Xl66kpl.gif",
"https://i.imgur.com/u7EIIVr.gif",
"https://i.imgur.com/jc1JoqM.gif",
"https://i.imgur.com/mpwsnrx.gif",
"https://i.imgur.com/NtdhV7E.gif",
"https://i.imgur.com/p4mSV6o.gif",
"https://i.imgur.com/9kLu8fE.gif",
"https://i.imgur.com/LJ73GB8.gif",
"https://i.imgur.com/gexziuO.gif",
"https://i.imgur.com/meqWOgW.gif",
"https://i.imgur.com/K3PPVKp.gif",
"https://i.imgur.com/PGGvVkv.gif",
"https://i.imgur.com/4sHq5Nv.gif",
"https://i.imgur.com/nStYugX.gif",
"https://i.imgur.com/GI7LuCN.gif",
"https://i.imgur.com/wqMSAUv.gif",
"https://i.imgur.com/uJnlAtC.gif",
"https://i.imgur.com/nTxBVbb.gif"
]

# Array of self high five gif URLs
self_high_five_gifs = [
"https://i.imgur.com/7RipXt1.gif",
"https://i.imgur.com/NrbO409.gif",
"https://i.imgur.com/4XHZA9m.gif",
"https://i.imgur.com/oScaUrQ.gif",
"https://i.imgur.com/EtgLwDc.gif"
]

# Array of denied high five gif URLs
denied_high_five_gifs = [
"https://i.imgur.com/4yGJHZP.gif",
"https://i.imgur.com/0pRyGCr.gif",
"https://i.imgur.com/vVXl2va.gif",
"https://i.imgur.com/HoVND9X.gif",
"https://i.imgur.com/yIU4s2o.gif",
"https://i.imgur.com/yevDlYT.gif",
"https://i.imgur.com/a1KUSZl.gif",
"https://i.imgur.com/YbikylC.gif",
"https://i.imgur.com/71wcWKP.gif",
"https://i.imgur.com/RM5V8hs.gif",
"https://i.imgur.com/s4qdMYk.gif",
"https://i.imgur.com/NDmnUgU.gif",
"https://i.imgur.com/5NWgfnk.gif",
"https://i.imgur.com/JHWNzVz.gif",
"https://i.imgur.com/ZswMzhh.gif",
"https://i.imgur.com/rTQlODg.gif",
"https://i.imgur.com/K5Bhex2.gif"
]

# Define command handlers here.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='ShruggieBot can shrug.\nUse /shruggie to shrug')


def halp(bot, update):
    halp_text = """
ShruggieBot can shrug and also other things

/shruggie - shrug
/sadshruggie - sad shrug
/lenny - Lenny face
/diretide - GIVE DIRETIDE
/helix - USE HELIX
/ayy - ayy
/flip - flip a table
/unflip - unflip a table
/disapprove - disapproving face
/YEAH _[optional: setup text]_ ; _[optional: punchline text]_ - CSI Miami Simulator 2016
/fives - high five with another user in this chat
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
        # Wait 5 seconds
        # TODO Implement non-blocking way to wait
        time.sleep(5)
        
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


def high_five(bot, update):
    # If this is the first /five in the last minute, add it to the list and start a countdown thread (_high_five_timeout).
    # If this is the second /five, post a normal high five gif if it wasn't the same person or a self high five if the user IDs ==.
    # This doesn't really matter so we don't save it to file in case of restarts
    chat_index = None
    for index, item in enumerate(last_high_five_time):
        if item[0] == update.message.chat_id:
            chat_index = index
            break
            
    # Add this chat if it wasn't found, this is the first high five
    if chat_index is None:
        logger.info('Initiate high five in chat %s' % (update.message.chat_id))
        last_high_five_time.append((update.message.chat_id, update.message.from_user.id, datetime.now()))
        
        try:
           thread.start_new_thread(_high_five_timeout, (bot, update.message.chat_id, update.message.message_id, ) )
        except:
            logger.info('Error: unable to start _high_five_timeout thread')
        
    else:
        if datetime.now() < (last_high_five_time[chat_index][2] + timedelta(seconds=60)):
            if last_high_five_time[chat_index][1] == update.message.from_user.id:
                # Get a random self high five gif
                logger.info('Self high five in chat %s' % (update.message.chat_id))
                high_five_gif = self_high_five_gifs[random.randint(0,len(self_high_five_gifs) - 1)]
            else:
                # Get a random normal high five gif
                logger.info('Normal high five in chat %s' % (update.message.chat_id))
                high_five_gif = normal_high_five_gifs[random.randint(0,len(normal_high_five_gifs) - 1)]
            
            # Post the gif
            bot.sendVideo(update.message.chat_id, text='/fives', video=high_five_gif)
            
        # Remove the previous high five entry
        last_high_five_time.pop(chat_index)
        

def _high_five_timeout(bot, chat_id, message_id):
    time.sleep(60)
    
    chat_index = None
    for index, item in enumerate(last_high_five_time):
        if item[0] == chat_id:
            logger.info('Denied high five in chat %s' % (chat_id))
            
            last_high_five_time.pop(index)
            high_five_gif = denied_high_five_gifs[random.randint(0,len(denied_high_five_gifs) - 1)]
            bot.sendVideo(chat_id, text='/fives', video=high_five_gif, reply_to_message_id=message_id)
            break


#
# Returns a list of 0, 1, or 2 length args split apart by ";"
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
    
    logger.info('Starting shruggiebot')

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # On different commands, answer in Telegram
    dispatch.addHandler(CommandHandler("start", start))
    dispatch.addHandler(CommandHandler("help", halp))
    dispatch.addHandler(CommandHandler("halp", halp))
    dispatch.addHandler(CommandHandler("shrug", shruggie))
    dispatch.addHandler(CommandHandler("shug", shruggie)) # Typos = hard
    dispatch.addHandler(CommandHandler("shruggie", shruggie))
    dispatch.addHandler(CommandHandler("shuggie", shruggie))
    dispatch.addHandler(CommandHandler("sadshrug", sad_shruggie))
    dispatch.addHandler(CommandHandler("sadshruggie", sad_shruggie))
    dispatch.addHandler(CommandHandler("lenny", lenny))
    dispatch.addHandler(CommandHandler("diretide", diretide))
    dispatch.addHandler(CommandHandler("helix", helix))
    dispatch.addHandler(CommandHandler("ayy", ayy))
    dispatch.addHandler(CommandHandler("flip", flip))
    dispatch.addHandler(CommandHandler("unflip", unflip))
    dispatch.addHandler(CommandHandler("disapprove", disapprove))
    dispatch.addHandler(CommandHandler("yeah", yeah))
    dispatch.addHandler(CommandHandler("YEAH", yeah))
    dispatch.addHandler(CommandHandler("DOORSLAM", doorslam))
    dispatch.addHandler(CommandHandler("five", high_five))
    dispatch.addHandler(CommandHandler("fives", high_five))
    dispatch.addHandler(CommandHandler("efive", high_five))
    dispatch.addHandler(CommandHandler("efives", high_five))
    dispatch.addHandler(CommandHandler("highfive", high_five))
    dispatch.addHandler(CommandHandler("highfives", high_five))

    # Log all errors
    dispatch.addErrorHandler(error)
    
    # Start the bot
    updater.start_polling()

    # Run the bot until the you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
    logger.info('Stopping shruggiebot')

if __name__ == '__main__':
    main()
