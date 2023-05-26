from os import environ, listdir
import discord
from bs4 import BeautifulSoup
from requests import get
from discord.ext import commands
import alive
TOKEN = environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category = 'Misc Commands')


class MyBot(commands.Bot):
  async def setup_hook(self):
    print(f"Logging in as: {self.user}")
    
    print("=" * 50)
    print("--- Attempting to load all cogs... --- ")
    for filename in listdir("./cogs"):
        if filename.endswith('.py'):
            print(f"Attempting to load {filename}")
            await self.load_extension(f'cogs.{filename[:-3]}')
            print(f"Successfully loaded {filename}")
    print("=" * 50)
    
    print(f"{self.user} has successfully connected! Use prefix {self.command_prefix}")
    alive.keep_alive()
    
bot = MyBot(command_prefix=commands.when_mentioned_or('('), intents=intents, help_command = help_command, activity = discord.Game(name="with Epitaph | (help"))



@bot.command(brief="Reloads all cogs", description="Reloads all cogs")
async def reload(ctx): 
  if ctx.author.id == 0: # replace with your discord ID, or whoever you want to be able to reload your cogs
    for filename in listdir("./cogs"):
        if filename.endswith('.py'):
            try:
                await bot.unload_extension(f'cogs.{filename[:-3]}')
            except:
                continue
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send(f"Successfully reloaded `{filename}`")
  else:
    return 0


@bot.command(brief="Scrapes HTML from webpage")
@commands.cooldown(1, 4, commands.BucketType.user)
async def scrape(ctx, page):
    req_page = get(page)
    req_page = BeautifulSoup(req_page.content, 'html.parser')
    soup_page = req_page.prettify()
    with open("scraped_page.html", "w", encoding='utf-8') as file:
        file.write(str(soup_page))
    await ctx.send(file=discord.File('scraped_page.html'))


bot.run(TOKEN)
