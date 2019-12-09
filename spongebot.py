import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import pyshorteners
from pyshorteners import Shorteners

bot_on = True

# Scrapes google images for a specified input
def find_sb_reference(message):
    url = "https://www.google.com/search?q=Spongebob" + " " + message + "&safe=active&sxsrf=ACYBGNTyWYkdc3rQDOfPTFinpBDT55OP2Q:1575598277416&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjJ9Yj9-J_mAhXiQd8KHaNSALcQ_AUoAnoECAEQBA&biw=1440&bih=700"

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    for raw_img in soup.find_all('img'):
      link = raw_img.get('src')
      if link:
        if ".png" in link or ".jpg" in link:
            continue
        return link

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



# Replies to other messages with a link to a spongebob image. There is a cool down
@client.event
async def on_message(message):
    global bot_on

    if bot_on and not message.content.startswith('!'):
        if client.user.id != message.author.id:
            channel = message.channel

            if not has_bad_word(message.content):
                the_link = find_sb_reference(message.content)
                the_link = shortened(the_link)
                await channel.send(the_link)
    await client.process_commands(message) # necessary when mixing on_messsage with commands

# turns the bot on
@client.command()
async def spongebot(ctx):
    global bot_on
    if not bot_on:
        bot_on = True
        await ctx.send("I'm ready!!!")

# turns the bot off
@client.command()
async def off(ctx):
    global bot_on
    if bot_on:
        bot_on = False
        await ctx.send("Okay, bye!")

# Runs the bot on discord
client.run('INSERT_API_KEY_HERE')
