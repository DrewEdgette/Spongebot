import discord
from discord.ext import commands
import pyshorteners
from pyshorteners import Shorteners
import praw
import random

bot_on = True

# uses the reddit api to search for spongebob memes on r/BikiniBottomTwitter
def get_reply_and_image(message):
    reddit = praw.Reddit(client_id='insert your client id',
                         client_secret='insert your client secret',
                         user_agent='insert your user_agent')

    bbt = reddit.subreddit("BikiniBottomTwitter")

    url_list = {}
    for post in bbt.search(message, limit=5):
        link = post.url
        title = post.title
        if "imgur.com" in link:
            link += ".jpg"
        if ".png" in link or ".jpg" in link:
            url_list[title] = link

    if len(url_list) == 0:
        title = ""
        url = 1
    else:
        title = random.choice(list(url_list.keys()))
        url = url_list[title]

    return(title,url)


# Just so I'm not googling bad things
def has_bad_word(message):
    try:
        with open("badwords.txt") as f:
            bad_words = f.readlines()
            bad_words = [x.strip() for x in bad_words]

        message = message.lower()

        for word in bad_words:
            if word in message:
                return True
        return False
    except FileNotFoundError:
        raise


# Shortens the google image url
def shortened(url):
    try:
        s = pyshorteners.Shortener(Shorteners.TINYURL)
        short_url = s.short(url)
    except TypeError as err:
        return "I can't PBTTHH understand PBTTHH your accent"
    else:
        return short_url


# Initiates the bot
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Spongebot is online')



# Replies to other messages with a link to a spongebob meme
@client.event
async def on_message(message):
    global bot_on

    reserved_words = ["!spongebot", "!off"]

    if message.content in reserved_words:
        await client.process_commands(message)
    else:
        if bot_on:
            if client.user.id != message.author.id:
                if message.content.startswith("!"):
                    channel = message.channel

                    msg = message.content
                    msg = msg[1:]

                    if not has_bad_word(msg):
                        (reply,url) = get_reply_and_image(msg)
                        url = shortened(url)

                        if reply == "":
                            await channel.send(url)
                            return

                        await channel.send(reply)
                        await channel.send(url)




# turns the bot on
@client.command()
async def spongebot(ctx):
    global bot_on
    if not bot_on:
        bot_on = True
        await ctx.send("I'm ready!!!\n Here are all of my commands:\n !spongebot - turns me on\n !off - turns me off\n Type ! followed by anything else for a spongebob picture.")

# turns the bot off
@client.command()
async def off(ctx):
    global bot_on
    if bot_on:
        bot_on = False
        await ctx.send("Okay, bye!")

# Runs the bot on discord
client.run('insert your API key here') # - Spongebot Squarepants
