import os
 # write your code here and run "python main.py" in your terminal
# to stop running your code, just spam Ctrl+C in your terminal
import discord
import random
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
import urllib
import alive
TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=intents, help_command = help_command, activity = discord.Game(name="with Epitaph | $help"))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! It took {round(client.latency*1000)} ms to send this message!")

@client.command()
async def ball(ctx, *, question):
    possible_answers = ["No.", "Yes.", "Maybe.", "Possibly.", "Is the sky blue?", "I cannot say for sure.", "Why are you asking me that?", "I have no idea.", "Ask again later.", "Fuck no.", "You're one of those, aren't you?", "It is certain.", "Most likely.", "Outlook good.", "Outlook bad."]
    answer = random.choice(possible_answers)
    await ctx.send(f'The answer to your question "{question}"... {answer}')
    
@client.command()
async def id(ctx, user=None):
    if user == None:
        await ctx.send(f"Your ID is: {ctx.message.author.id}")
    else:
        checkuserid = int(ctx.message.content[6:-1])
        await ctx.send(f"Requested ID is: {checkuserid}")

@client.command()
async def rate(ctx, *, user=None):
    num = random.randint(1, 10)
    if user == None:
        await ctx.send(f"You have been rated as {num}/10.")
    elif "<@" in user:
        userid = int(ctx.message.content[8:-1])
        userid = str(userid)
        await ctx.send(f"<@{userid}> has been rated as {num}/10.")
    else: 
        await ctx.send(f"{user} has been rated as {num}/10.")


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
async def search(ctx, *, query):
    template = "https://www.thebrpage.net/discography/search.asp?search="
    template2 = "https://www.thebrpage.net/discography/"
    new_query = urllib.parse.quote_plus(query)
    new_query = new_query.replace('"', "")
    new_query = new_query.lower()
    full_page = f"{template}{new_query}"
    page_text = requests.get(full_page)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    soup_page = page_text.prettify()
    links = []
    value = 0
    for link in page_text.findAll('a'):
        links.append(link.get('href'))
    filtered_links = []
    result_links = []
    super_result_links = []
    for link in links:
        if link != None:
            filtered_links.append(link)
    for flink in filtered_links:
        flinck = flink.replace(" ", "+")
        if "catID" in flink or "user" in flink or "contributors" in flink or "songs.asp" in flink:
            filtered_links.remove(flink) 
        else:
            result_links.append(flinck)
    for thing in result_links:
        if "discography" in thing or "variation" in thing or "song.asp" in thing:
            super_result_links.append(thing)
    for thing in super_result_links:
        if "variation" not in thing and "song.asp" not in thing:
            super_result_links.remove(thing)
    for thing in super_result_links:
        if "img" in thing:
            super_result_links.remove(thing)
    super_result_links.remove(super_result_links[0])
    link_str = ""
    link_str2 = ""
    link_str3 = ""
    link_str4 = ""
    link_str5 = ""
    link_number = 1
    for link in super_result_links:
        link_str += f"{link_number}: {template2}{link}"
        link_str += "\n"
        link_number += 1
        super_result_links.remove(link)
        if link_number > 10:
            break
    for link in super_result_links:
        link_str2 += f"{link_number}: {template2}{link}"
        link_str2 += "\n"
        link_number += 1
        super_result_links.remove(link)
        if link_number > 20:
            break
    for link in super_result_links:
        link_str3 += f"{link_number}: {template2}{link}"
        link_str3 += "\n"
        link_number += 1
        super_result_links.remove(link)
        if link_number > 30:
            break
    for link in super_result_links:
        link_str4 += f"{link_number}: {template2}{link}"
        link_str4 += "\n"
        link_number += 1
        super_result_links.remove(link)
        if link_number > 40:
            break
    for link in super_result_links:
        link_str5 += f"{link_number}: {template2}{link}"
        link_str5 += "\n"
        link_number += 1
        super_result_links.remove(link)
        if link_number > 50:
            break
    search_embed = discord.Embed(title=f'Search results for "{query}"', url=full_page, description=f"{link_str}")
    search_embed2 = discord.Embed(title=f'Search results for "{query}"', url=full_page, description=f"{link_str2}")
    search_embed3 = discord.Embed(title=f'Search results for "{query}"', url=full_page, description=f"{link_str3}")
    search_embed4 = discord.Embed(title=f'Search results for "{query}"', url=full_page, description=f"{link_str4}")
    search_embed5 = discord.Embed(title=f'Search results for "{query}"', url=full_page, description=f"{link_str5}")
    pages = [search_embed,search_embed2, search_embed3, search_embed4, search_embed5]
    search_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    search_embed2.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    search_embed3.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    search_embed4.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    search_embed5.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    message = await ctx.send(embed=search_embed)
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')
    def check(reaction, user):
        return user == ctx.author
    i = 0
    reaction = None
    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < 4:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = 4
            await message.edit(embed = pages[i])
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 120.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break
    await message.clear_reactions()

@client.command()
async def qotd(ctx):
    qotd_info = []
    main_page = "https://www.thebrpage.net/"
    page_text = requests.get(main_page)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    soup_page = page_text.prettify()
    with open("main_page.txt", "w") as file:
        file.write(str(soup_page))
    with open("main_page.txt", "r") as file:
        data = file.read()
        data_list = data.split("\n")
        data_list_iter = iter(data_list)
    for line in data_list_iter:
        if '<div id="quoteoftheday">' in line:
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
            qotd_info.append(next(data_list_iter))
    for thing in qotd_info:
        if "<" in thing or "     :" in thing or "      -" in thing:
            qotd_info.remove(thing)
    qotd_info.remove(qotd_info[1])
    quote = qotd_info[1]
    song_title = qotd_info[4]
    song_title = song_title.strip( )
    new_title = urllib.parse.quote_plus(song_title)
    new_title = new_title.replace('"', "")
    new_title = new_title.title()
    song_link = f"https://www.thebrpage.net/discography/song.asp?songName={new_title}"
    song_embed = discord.Embed(title=song_title.title(), url=song_link, description=f"{quote}")
    song_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
    await ctx.send(embed=song_embed)

@client.command()
async def song(ctx, song_title: str, info="no"):
    num = random.randint(1, 10)
    info = info.lower()
    template = "https://www.thebrpage.net/discography/song.asp?songName="
    template2 = "https://www.thebrpage.net/discography/"
    new_title = urllib.parse.quote_plus(song_title)
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
    elif info == "releases" or info == "r" or info == "versions" or info == "v":
      song_versions = []
      with open(f"scraped_song{num}.txt", "r") as file:
        data = file.read()
        data_list = data.split("\n")
        data_list_iter = iter(data_list)
      for line in data_list_iter:
        if '<a href="variation.asp?varID=' in line:
          line2 = line.strip( )
          line3 = line2.replace('itemprop="inAlbum">', '')
          line4 = line3.rstrip(line3[-1])
          song_versions.append(line4.replace('<a href="', ''))
      link_str = ""
      link_str2 = ""
      link_str3 = ""
      link_str4 = ""
      link_str5 = ""
      link_number = 1
      for link in song_versions:
          link_str += f"{link_number}: {template2}{link}"
          link_str += "\n"
          link_number += 1
          song_versions.remove(link)
          if link_number > 10:
              break
      for link in song_versions:
          link_str2 += f"{link_number}: {template2}{link}"
          link_str2 += "\n"
          link_number += 1
          song_versions.remove(link)
          if link_number > 20:
              break
      for link in song_versions:
          link_str3 += f"{link_number}: {template2}{link}"
          link_str3 += "\n"
          link_number += 1
          song_versions.remove(link)
          if link_number > 30:
              break
      for link in song_versions:
          link_str4 += f"{link_number}: {template2}{link}"
          link_str4 += "\n"
          link_number += 1
          song_versions.remove(link)
          if link_number > 40:
              break
      for link in song_versions:
          link_str5 += f"{link_number}: {template2}{link}"
          link_str5 += "\n"
          link_number += 1
          song_versions.remove(link)
          if link_number > 50:
              break
      title_title = song_title.title()
      ver_embed = discord.Embed(title=f'Releases featuring "{title_title}"', url=full_page, description=f"{link_str}")
      ver_embed2 = discord.Embed(title=f'Releases featuring "{title_title}"', url=full_page, description=f"{link_str2}")
      ver_embed3 = discord.Embed(title=f'Releases featuring "{title_title}"', url=full_page, description=f"{link_str3}")
      ver_embed4 = discord.Embed(title=f'Releases featuring "{title_title}"', url=full_page, description=f"{link_str4}")
      ver_embed5 = discord.Embed(title=f'Releases featuring "{title_title}"', url=full_page, description=f"{link_str5}")
      pages = [ver_embed, ver_embed2, ver_embed3, ver_embed4, ver_embed5]
      ver_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      ver_embed2.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      ver_embed3.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      ver_embed4.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      ver_embed5.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      message = await ctx.send(embed=ver_embed)
      await message.add_reaction('⏮')
      await message.add_reaction('◀')
      await message.add_reaction('▶')
      await message.add_reaction('⏭')
      def check(reaction, user):
          return user == ctx.author
      i = 0
      reaction = None
      while True:
          if str(reaction) == '⏮':
              i = 0
              await message.edit(embed = pages[i])
          elif str(reaction) == '◀':
              if i > 0:
                  i -= 1
                  await message.edit(embed = pages[i])
          elif str(reaction) == '▶':
              if i < 4:
                  i += 1
                  await message.edit(embed = pages[i])
          elif str(reaction) == '⏭':
              i = 4
              await message.edit(embed = pages[i])
          try:
              reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
              await message.remove_reaction(reaction, user)
          except:
              break
      await message.clear_reactions()
    elif info == "info" or info == "i":
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
        if "<" in author:
            author = "N/A"
        release_date = song_info[5]
        if "<" in release_date:
            release_date = "N/A"
        bpm = song_info[8]
        if "<" in bpm:
            bpm = "N/A"
        song_embed = discord.Embed(title=song_title.title(), url=full_page, description=f"**Written by:** {author} \n**Release Date:** {release_date} \n**BPM:** {bpm}")
        song_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
        if "An error occurred" in page_text_str:
            await ctx.send("This song does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(embed=song_embed)

@client.command()
async def album(ctx, album_id: str, info="no"):
    tracks = []
    num = random.randint(1, 10)
    info = info.lower()
    template = "https://www.thebrpage.net/discography/item.asp?itemID="
    full_page = f"{template}{album_id}"
    page_text = requests.get(full_page)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    soup_page = page_text.prettify()
    page_text_str = str(page_text)
    with open(f"scraped_album{num}.txt", "w") as file:
        file.write(str(soup_page))
    if info == "no":
        if "An error occurred" in page_text_str:
            await ctx.send("This album does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(str(full_page))
    elif info == "info" or info == "i":
        with open(f"scraped_album{num}.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
            data_list_iter = iter(data_list)
        for line in data_list_iter:
            if '<td class="coloredLink" valign="top">' in line:
                tracks.append(next(data_list_iter))
                tracks.append(next(data_list_iter))
        for track in tracks:
            if "<" in track:
                tracks.remove(track)
        track_number = 1
        album_title = page_text.find('div', class_='pageTitle').text.strip()
        tracklist = ""
        for track in tracks:
            tracklist += f"\n{track_number}: {track}"
            track_number += 1
        album_embed = discord.Embed(title=album_title, url=full_page, description=f"**Tracklist** {tracklist}")
        album_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
        if "An error occurred" in page_text_str:
            await ctx.send("This song does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(embed=album_embed)
        
@client.command()
async def release(ctx, release_id, info="no"):
    num = random.randint(1, 10)
    info = info.lower()
    template = "https://www.thebrpage.net/discography/variation.asp?varID="
    id = int(release_id)
    full_page = f"{template}{id}"
    page_text = requests.get(full_page)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    soup_page = page_text.prettify()
    page_text_str = str(page_text)
    with open(f"scraped_version{num}.txt", "w") as file:
        file.write(str(soup_page))
    if info == "no":
        if "An error occurred" in page_text_str:
            await ctx.send("This release does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(str(full_page))
    elif info == "info" or info == "i":
        release_info = []
        release_info2 = []
        release_title = page_text.find('div', class_='pageTitle').text.strip()
        with open(f"scraped_version{num}.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
            data_list_iter = iter(data_list)
        for line in data_list_iter:
            if '<td style="f' in line:
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
                release_info.append(next(data_list_iter))
        label = release_info[3]
        if "<" in label:
            label = "N/A"
        release_date = release_info[9]
        if "<" in release_date:
            release_date = "N/A"
        country = release_info[13]
        if "<" in country:
            country = "N/A"
        details = release_info[19]
        if "<" in details:
            details = "N/A"
        release_format = release_info[23]
        if "<" in release_format:
            release_format = "N/A"
        release_embed = discord.Embed(title=release_title, url=full_page, description=f"**Label:** {label} \n**Release Date:** {release_date} \n**Country:** {country} \n**Disc/Label Details:** {details} \n**Format:** {release_format}")
        release_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
        if "An error occurred" in page_text_str:
            await ctx.send("This release does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(embed=release_embed)
        

alive.keep_alive()
client.run(TOKEN)
