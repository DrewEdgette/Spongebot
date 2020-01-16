import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import pyshorteners
from pyshorteners import Shorteners
import random

bot_on = True

# Scrapes spongebob fandom for a specified input
def get_search_link(message):
    url = "https://spongebob.fandom.com/wiki/Special:Search?query=" + message
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")


    for result_link in soup.find_all("a","result-link"):
        link = result_link.get("href")
        if link:
            return link
        else:
            continue
    return 1


# once the page is found, we can grab an image from it
def get_image_link(result_link):
    if result_link == 1:
        return 1
    url = result_link
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    img_links = soup.find_all("img")[1:5]

    while True:
        if len(img_links) == 0:
            return

        rdm_link = random.choice(img_links)
        link = rdm_link.get("src")

        if "gif" not in link:
            return link
        else:
            img_links.remove(rdm_link)
            continue
    return 1


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


# Shortens the url
def shortened(url):
    try:
        s = pyshorteners.Shortener(Shorteners.TINYURL)
        short_url = s.short(url)
    except TypeError as err:
        return "I can't PBTTHH understand PBTTHH your accent"
    else:
        return short_url


# Initiates the bot
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Spongebot is online")



# Replies to other messages with a link to a spongebob image.
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
                        search_link = get_search_link(msg)
                        image_link = get_image_link(search_link)
                        image_link = shortened(image_link)
                        await channel.send(image_link)



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
client.run("insert your API key here") # - Spongebot Squarepants
