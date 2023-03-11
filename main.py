import discord
import random
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=intents, help_command = help_command, activity = discord.Game(name="with Epitaph"))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! It took {round(client.latency*1000)} ms to send this message!")

@client.command()
async def greet(ctx):
    greetings = ["Hiya!", "Hi!", "Hello!", "What's up?", "Hey!", "Heya!", "Haiii!!! ^-^"]
    await ctx.send(random.choice(greetings))

@client.command()
async def scrape(ctx, page):
    num = random.randint(1, 10)
    req_page = requests.get(page)
    req_page = BeautifulSoup(req_page.content, 'html.parser')
    soup_page = req_page.prettify()
    with open(f"scraped_page{num}.html", "w", encoding='utf-8') as file:
        file.write(str(soup_page))
    await ctx.send(file=discord.File(f'scraped_page{num}.html'))

@client.command()
async def br_song(ctx, song_title: str, info="no"):
    num = random.randint(1, 10)
    template = "https://www.thebrpage.net/discography/song.asp?songName="
    new_title = song_title.replace(" ", "+")
    new_title = new_title.replace('"', "")
    new_title = new_title.lower()
    full_page = f"{template}{new_title}"
    page_text = requests.get(full_page)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    soup_page = page_text.prettify()
    page_text_str = str(page_text)
    with open(f"scraped_song{num}.txt", "w") as file:
        file.write(str(soup_page))
    if info == "no":
        if "An error occurred" in page_text_str:
            await ctx.send("This song does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(str(full_page))
    elif info == "info":
        song_info = []
        with open(f"scraped_song{num}.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
            data_list_iter = iter(data_list)
            for line in data_list_iter:
                if '<td style="f' in line:
                    song_info.append(next(data_list_iter))
                    song_info.append(next(data_list_iter))
                    song_info.append(next(data_list_iter))
                    song_info.append(next(data_list_iter))
                    song_info.append(next(data_list_iter))
        for thing in song_info:
            if "</td>" in thing or "<td>" in thing:
                song_info.remove(thing)
        author = song_info[2]
        release_date = song_info[5]
        bpm = song_info[8]
        song_embed = discord.Embed(title=song_title.title(), url=full_page, description=f"Written by: {author} \nRelease Date: {release_date} \nBPM: {bpm}")
        await ctx.send(embed=song_embed)
    elif info == "lyrics":
        pass

client.run('TOKEN')
