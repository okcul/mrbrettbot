import os
import discord
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
import alive #ONLY USE IF YOU ARE ON REPLIT AND CREATING A WEBSERVER USING FLASK AND THREADING
TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category = 'Misc Commands')
bot = commands.Bot(command_prefix=commands.when_mentioned_or('('), intents=intents, help_command = help_command, activity = discord.Game(name="with Epitaph | (help"))

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send("This command is currently on cooldown for {:.2f} more seconds.".format(error.retry_after))
  else:
    await ctx.send("idk you got some random error")

@bot.command(brief="Reloads all cogs", description="Reloads all cogs")
async def reload(ctx): 
  if ctx.author.id == YOUR_DISCORD_ID_HERE:
    for filename in os.listdir("./cogs"):
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
    req_page = requests.get(page)
    req_page = BeautifulSoup(req_page.content, 'html.parser')
    soup_page = req_page.prettify()
    with open(f"scraped_page.html", "w", encoding='utf-8') as file:
        file.write(str(soup_page))
    await ctx.send(file=discord.File(f'scraped_page{num}.html'))

alive.keep_alive()
bot.run(TOKEN)
