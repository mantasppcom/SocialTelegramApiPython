import os
import telebot
import vk
import variables
import twitch
import weather
import twitter
import tweepy
import youtube
from telebot import types
from flask import Flask, request


__author__ = 'Rustam Gasanov'
__version__ = '1.0'

server = Flask(__name__)
bot = telebot.TeleBot(variables.TOKEN)
method_name = 'wall.get'
domain = ''
channel_name = ''
city_name = ''
screen_name = ''
youtube_channel = ''
commands = {'cityname': 'example: /cityname Kiev',
            'weather': 'send weather information',
            'twitch': 'example: /twitch gnumme',
            'channelinfo': 'send information about channel',
            'randomvideo': 'send random channel video',
            'lastvideo': 'send last channel video',
            'vk': 'example: /vk igm',
            'randompost': 'send random group post',
            'lastpost': 'send last group post',
            'randomphoto': 'send random group photo',
            'gif': 'send random group gif',
            'vkvideo': 'send random group video',
            'twitter': 'example: /twitter wylsacom',
            'randomtweet': 'send random user tweet',
            'lasttweet': 'send last user tweet',
            'youtube': 'example: /youtube wylsacom',
            'youtuberandom': 'send random channel video',
            'youtubelast': 'send last channel video'
}


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Examples: \n/youtube wylsacom, \n/vk igm, ' +
             '\n/twitch gnumme, \n/twitter durov, \n/cityname London .'
    )

################################################################################
                                #YOUTUBE

@bot.message_handler(commands=['youtube'])
def new_youtube(message):
    global youtube_channel
    youtube_channel = message.text[len('/youtube') + 1:]

    try:
        youtube.youtube_main(youtube_channel)
    except IndexError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )

    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='You choose channel with name youtube_channel.'
        )

        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        )

        random = types.KeyboardButton('/youtuberandom')
        last = types.KeyboardButton('/youtubelast')
        markup.add(random, last)

        bot.send_message(
            chat_id=message.chat.id,
            text='Choose command: ',
            reply_markup=markup
        )

@bot.message_handler(commands=['youtuberandom'])
def youtuberandom(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of youtube_channel video',
            url=youtube.youtube_main(youtube_channel)[0]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + youtube.youtube_main(youtube_channel)[0] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except IndexError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )

    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )

@bot.message_handler(commands=['youtubelast'])
def youtubelast(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + youtube_channel + ' video',
            url=youtube.youtube_main(youtube_channel)[1]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + youtube.youtube_main(youtube_channel)[1] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except IndexError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )

    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist or channel have not video.'
        )


################################################################################
                                #TWITTER

@bot.message_handler(commands=['twitter'])
def new_twitter(message):
    global screen_name
    screen_name = message.text[len('/twitter') + 1:]
    try:
        twitter.twitter_main(screen_name)
    except tweepy.error.TweepError:

        bot.send_message(
            chat_id=message.chat.id,
            text='User does not exist or user have not tweets.'
        )

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='You choose user with name: ' + screen_name + '.'
        )

        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        )

        random = types.KeyboardButton('/randomtweet')
        last = types.KeyboardButton('/lasttweet')
        markup.add(random, last)

        bot.send_message(
            chat_id=message.chat.id,
            text='Choose command: ',
            reply_markup=markup
        )

@bot.message_handler(commands=['randomtweet'])
def random_tweet(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + screen_name + ' tweet',
            url=twitter.twitter_main(screen_name).generate_tweet_link()[0]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + twitter.twitter_main(screen_name).generate_tweet_link()[0] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except tweepy.error.TweepError:
        bot.send_message(
            chat_id=message.chat.id,
            text='User does not exist or user' + 'have not tweets.'
        )

    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text='User does not exist or user' + 'have not tweets.'
        )

@bot.message_handler(commands=['lasttweet'])
def last_tweet(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + screen_name + ' tweet',
            url=twitter.twitter_main(screen_name).generate_tweet_link()[1]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + twitter.twitter_main(screen_name).generate_tweet_link()[1] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text='User does not exist or user' + 'have not tweets.'
        )

    except tweepy.error.TweepError:
        bot.send_message(
            chat_id=message.chat.id,
            text='User does not exist or user' + 'have not tweets.'
        )


################################################################################
                                #WEATHER

@bot.message_handler(commands=['cityname'])
def city_name(message):
    global city_name
    city_name = message.text[len('/cityname') + 1:]
    w = weather.Weather(city_name, variables.KEY)
    bot.send_message(
        chat_id=message.chat.id,
        text='You choose ' + city_name + ' city.'
    )

    try:
        coordinates = w.get_coordinates()
        bot.send_location(
            chat_id=message.chat.id,
            latitude=coordinates[0],
            longitude=coordinates[1]
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='City does not exist.'
        )

    else:
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        )

        weather_information = types.KeyboardButton('/weather')
        markup.add(weather_information)

        bot.send_message(
            chat_id=message.chat.id,
            text='Choose command: ',
            reply_markup=markup
        )

@bot.message_handler(commands=['weather'])
def new_weather(message):
    w = weather.Weather(city_name, variables.KEY)
    try:
        weather_information = w.get_weather()
        bot.send_message(
            chat_id=message.chat.id,
            text='Temperature - ' + weather_information[0] +
                 ' *C, \nhumidity - ' + weather_information[1] +
                 ' %, \nspeed of wind - ' + weather_information[2] + ' m/s.'
            )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='City does not exist.'
        )


################################################################################
                                #TWITCH

@bot.message_handler(commands=['twitch'])
def twitch_channel(message):
    global channel_name
    channel_name = message.text[len('/twitch') + 1:]
    t = twitch.Twitch(channel_name)

    bot.send_message(
        chat_id=message.chat.id,
        text='You choose ' + channel_name + ' channel.'
    )

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )

    twitchinfo = types.KeyboardButton('/channelinfo')
    last_video = types.KeyboardButton('/lastvideo')
    random_video = types.KeyboardButton('/randomvideo')
    markup.add(twitchinfo, last_video, random_video)

    bot.send_message(
        chat_id=message.chat.id,
        text='Choose command: ',
        reply_markup=markup
    )

@bot.message_handler(commands=['channelinfo'])
def channel_info(message):
    t = twitch.Twitch(channel_name)
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + channel_name + ' channel',
            url='https://twitch.tv/{0}'.format(channel_name)
        )

        keyboard.add(url_button)

        information = t.get_information()

        bot.send_message(
            chat_id=message.chat.id,
            text='\nstatus - ' + information[0] +
                 ', \ngame - ' + information[1] +
                 ', \nviewers - ' + information[5] +
                 ', \nlanguage - ' + information[2] +
                 ', \nviews - ' + information[3] +
                 ', \nfollowers - ' + information[4] + '.',
            reply_markup=keyboard
        )

    except IndexError:
        bot.send_message(
            chat_id=message.chat.id,
            text='\nstatus - ' + information[0] +
                 ', \ngame - ' + information[1] +
                 ', \nlanguage - ' + information[2] +
                 ', \nviews - ' + information[3] +
                 ', \nfollowers - ' + information[4] + '.',
            reply_markup=keyboard
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Channel does not exist.'
        )

@bot.message_handler(commands=['lastvideo'])
def last_video(message):
    t = twitch.Twitch(channel_name)
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + channel_name + ' last video',
            url=t.get_video()[0]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + t.get_video()[0] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Video does not exist.'
        )

@bot.message_handler(commands=['randomvideo'])
def twitchvideo(message):
    t = twitch.Twitch(channel_name)
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + channel_name + ' last video',
            url=t.get_video()[1]
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + t.get_video()[1] + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Video does not exist.'
        )


################################################################################
                                    #VK

@bot.message_handler(commands=['vk'])
def vkgroup(message):
    global domain
    global method_name
    domain = message.text[len('/vk') + 1:]
    try:
        vk.vk_main(domain, method_name)

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Group does not exist.'
        )

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='You choose a ' + domain + ' group.'
        )

        if domain.startswith('-'):
            bot.send_message(
                chat_id=message.chat.id,
                text='You choose a' + ' group with id ' + domain + '.'
            )

        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        )

        random_post = types.KeyboardButton('/randompost')
        last_post = types.KeyboardButton('/lastpost')
        random_photo = types.KeyboardButton('/randomphoto')
        gif = types.KeyboardButton('/gif')
        vk_video = types.KeyboardButton('/vkvideo')
        markup.add(random_post, last_post, random_photo, gif, vk_video)

        bot.send_message(
            chat_id=message.chat.id,
            text='Choose command: ',
            reply_markup=markup
        )

@bot.message_handler(commands=['randompost'])
def random_post(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + domain + '\'s post',
            url=vk.vk_main(domain, method_name).generate_vk_post()
        )

        keyboard.add(url_button)
        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + vk.vk_main(domain, method_name).generate_vk_post() + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except TypeError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Post does not exist.'
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Group does not exist.'
        )


@bot.message_handler(commands=['lastpost'])
def last_post(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + domain + '\'s post',
            url=vk.vk_main(domain, method_name).generate_vk_last_post()
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + vk.vk_main(domain, method_name).generate_vk_last_post() + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except TypeError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Post does not exist.'
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Post does not exist.'
        )

@bot.message_handler(commands=['vkvideo'])
def vk_video(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + domain + '\'s video',
            url=vk.vk_main(domain, method_name).generate_vk_video()
        )

        keyboard.add(url_button)

        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + vk.vk_main(domain, method_name).generate_vk_video() + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except TypeError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Video does not exist.'
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Video does not exist.'
        )

@bot.message_handler(commands=['gif'])
def gif(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + domain + '\'s gif',
            url=vk.vk_main(domain, method_name).generate_vk_gif()
        )

        keyboard.add(url_button)
        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + vk.vk_main(domain, method_name).generate_vk_gif() + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except TypeError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Gif does not exist.'
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Gif does not exist.'
        )

@bot.message_handler(commands=['randomphoto'])
def random_photo(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
            text='Link of ' + domain + '\'s photo',
            url=vk.vk_main(domain, method_name).generate_vk_photo()
        )
        keyboard.add(url_button)
        bot.send_message(
            chat_id=message.chat.id,
            text='[.](' + vk.vk_main(domain, method_name).generate_vk_photo() + ')',
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    except TypeError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Photo does not exist.'
        )

    except KeyError:
        bot.send_message(
            chat_id=message.chat.id,
            text='Photo does not exist.'
        )

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://socialtelegrambot.herokuapp.com/bot")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)
