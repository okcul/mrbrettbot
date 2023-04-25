import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import random
import urllib
import re

async def setup(bot):
      await bot.add_cog(TheBRPage(bot))
  
class TheBRPage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def cog_unload(self):
        print('Cog Unloaded')

    async def get_images(self, list):
      for line in list:
        if 'image_src' in line:
          image_link = line
          image_link = re.findall(r'"(.*?)"', image_link)
          for link in image_link:
            if 'image_src' not in link:
              good_link = link
          good_link = good_link.replace(' ', '%20')
      try:
        return good_link
      except UnboundLocalError:
        good_link = 'https://www.thebrpage.net/img/thebrpage_logo_large.jpg'
        return good_link

    async def search_embed_setup(self, ctx, list, template, query, page, type):
      link_str = ""
      link_str2 = ""
      link_str3 = ""
      link_str4 = ""
      link_str5 = ""
      category = ""
      link_number = 1
      if type in ['show', 'sh']:
        category = "Shows"
      elif type in ['song', 's', 'release', 'r']:
        category = "Releases"
      elif type in ['merch', 'm', 'collectible', 'c']:
        category = "Merch"
      for link in list:
          link_str += f"{link_number}: {template}{link}"
          link_str += "\n"
          link_number += 1
          list.remove(link)
          if link_number > 10:
              break
      for link in list:
          link_str2 += f"{link_number}: {template}{link}"
          link_str2 += "\n"
          link_number += 1
          list.remove(link)
          if link_number > 20:
              break
      for link in list:
          link_str3 += f"{link_number}: {template}{link}"
          link_str3 += "\n"
          link_number += 1
          list.remove(link)
          if link_number > 30:
              break
      for link in list:
          link_str4 += f"{link_number}: {template}{link}"
          link_str4 += "\n"
          link_number += 1
          list.remove(link)
          if link_number > 40:
              break
      for link in list:
          link_str5 += f"{link_number}: {template}{link}"
          link_str5 += "\n"
          link_number += 1
          list.remove(link)
          if link_number > 50:
              break
      search_embed = discord.Embed(title=f'Search results for "{query}" in {category}', url=page, description=f"{link_str}")
      search_embed2 = discord.Embed(title=f'Search results for "{query}" in {category}', url=page, description=f"{link_str2}")
      search_embed3 = discord.Embed(title=f'Search results for "{query}" in {category}', url=page, description=f"{link_str3}")
      search_embed4 = discord.Embed(title=f'Search results for "{query}" in {category}', url=page, description=f"{link_str4}")
      search_embed5 = discord.Embed(title=f'Search results for "{query}" in {category}', url=page, description=f"{link_str5}")
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
              reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
              await message.remove_reaction(reaction, user)
          except asyncio.TimeoutError:
              break
      await message.clear_reactions()
      
    @commands.command(brief="Sends search results")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx, query, type):
        type = type.lower() 
        new_query = urllib.parse.quote_plus(query)
        new_query = new_query.replace('"', "")
        new_query = new_query.lower()
        links = []
        filtered_links = []
        result_links = []
        super_result_links = []
        if type in ['show', 'sh']:
          #SEARCH FOR SHOWS
          template = "https://www.thebrpage.net/shows/search_shows.asp?search="
          template2 = "https://www.thebrpage.net/shows/"
          full_page = f"{show_template}{new_query}"
          page_text = requests.get(full_page)
          page_text = BeautifulSoup(page_text.content, 'html.parser')
          for link in page_text.findAll('a'):
            try:
              if "details" not in link.get('title') and "setlist" not in link.get('title') and "video" not in link.get('title') and "comment" not in link.get('title') and "image" not in link.get('title'):
                links.append(link.get('href'))
            except:
              try:
                if "showID" in link.get('href'):
                  links.append(link.get('href'))
              except:
                continue
          for link in links:
              if link != None:
                  filtered_links.append(link)
          for flink in filtered_links:
              flinck = flink.replace(" ", "+")
              if "catID" in flink or "user" in flink or "contributors" in flink or "songs.asp" in flink or "comments" in flink:
                  filtered_links.remove(flink) 
              else:
                  result_links.append(flinck)
          for thing in result_links:
              if "show.asp" in thing and "showID" in thing:
                  super_result_links.append(thing)
              if "img" in thing:
                super_result_links.remove(thing)
          await self.search_embed_setup(ctx, super_result_links, template2, query, full_page, type)
        elif type in ['merch', 'm', 'collectible', 'c']:
          #SEARCH FOR MERCH
          template = "https://www.thebrpage.net/collectibles/search.asp?search="
          template2 = "https://www.thebrpage.net/collectibles/"
          full_page = f"{template}{new_query}"
          page_text = requests.get(full_page)
          page_text = BeautifulSoup(page_text.content, 'html.parser')
          for link in page_text.findAll('a'):
            links.append(link.get('href'))
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
              if "item.asp" in thing:
                  super_result_links.append(thing)
          for thing in super_result_links:
              if "img" in thing:
                  super_result_links.remove(thing)
          await self.search_embed_setup(ctx, super_result_links, template2, query, full_page, type)
          super_result_links.remove(super_result_links[0])
        elif type in ['song', 's', 'release', 'r']:
          #SEARCH FOR RELEASES
          template = "https://www.thebrpage.net/discography/search.asp?search="
          template2 = "https://www.thebrpage.net/discography/"
          full_page = f"{template}{new_query}"
          page_text = requests.get(full_page)
          page_text = BeautifulSoup(page_text.content, 'html.parser')
          for link in page_text.findAll('a'):
            links.append(link.get('href'))
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
          await self.search_embed_setup(ctx, super_result_links, template2, query, full_page, type)
    
    @commands.command(brief="Sends the QOTD")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def qotd(self, ctx):
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
                qotd_info.append(next(data_list_iter))
        for thing in qotd_info:
            if "<" in thing or "     :" in thing or "      -" in thing or "href=" in thing or "     <span class=" in thing:
                qotd_info.remove(thing)
            if thing == '     <span class="lightText">':
                qotd_info.remove(thing)
        qotd_info.remove(qotd_info[1])
        quote = qotd_info[1]
        song_title = qotd_info[4]
        song_title = song_title.strip( )
        new_title = urllib.parse.quote_plus(song_title)
        new_title = new_title.replace('"', "")
        new_title = new_title.title()
        song_link = f"https://www.thebrpage.net/discography/song.asp?songName={new_title}"
        page_text = requests.get(song_link)
        page_text = BeautifulSoup(page_text.content, 'html.parser')
        soup_page = page_text.prettify()
        with open("qotd_song.txt", "w") as file:
            file.write(str(soup_page))
        with open("qotd_song.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
        song_embed = discord.Embed(title=song_title.title(), url=song_link, description=f"{quote}")
        song_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
        song_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
        song_embed
        await ctx.send(embed=song_embed)
    
    @commands.command(brief="Sends song info")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def song(self, ctx, song_title: str, info="no"):
        info = info.lower()
        template = "https://www.thebrpage.net/discography/song.asp?songName="
        template2 = "https://www.thebrpage.net/discography/"
        new_title = urllib.parse.quote_plus(song_title)
        new_title = new_title.replace('"', "")
        new_title = new_title.lower()
        full_page = f"{template}{new_title}"
        page_text = requests.get(full_page)
        page_text2 = BeautifulSoup(page_text.content, 'html.parser')
        soup_page = page_text2.prettify()
        page_text_str = str(page_text2)
        with open(f"scraped_song.txt", "w") as file:
            file.write(str(soup_page))
        if info == "no":
            if "An error occurred" in page_text_str:
                await ctx.send("This song does not exist, or it does not have a page on the site.")
            else:
                await ctx.send(str(full_page))
        elif info == "releases" or info == "r" or info == "versions" or info == "v":
          song_versions = []
          with open(f"scraped_song.txt", "r") as file:
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
                  reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
                  await message.remove_reaction(reaction, user)
              except asyncio.TimeoutError:
                  break
          await message.clear_reactions()
        elif info == "info" or info == "i":
            song_info = []
            with open(f"scraped_song.txt", "r") as file:
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
            song_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
            if "An error occurred" in page_text_str:
              await ctx.send("This song does not exist, or it does not have a page on the site.")
            else:
              await ctx.send(embed=song_embed)
          
    
    @commands.command(brief="Sends show info")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def show(self, ctx, show_id, info="no"):
      num = random.randint(1,3)
      info = info.lower()
      template = "https://www.thebrpage.net/shows/show.asp?showID="
      new_title = urllib.parse.quote_plus(show_id)
      new_title = new_title.replace('"', "")
      new_title = new_title.lower()
      full_page = f"{template}{new_title}"
      page_text = requests.get(full_page)
      page_text = BeautifulSoup(page_text.content, 'html.parser')
      soup_page = page_text.prettify()
      show_title = page_text.find('div', class_='pageTitle').text.strip()
      page_text_str = str(page_text)
      with open(f"scraped_song.txt", "w") as file:
        file.write(str(soup_page))
      if info == "no":
        if "An error occurred" in page_text_str:
          await ctx.send("This show does not exist, or it does not have a page on the site.")
        else:
          await ctx.send(str(full_page))
      elif info == "info" or info == "i":
        show_info = []
        with open(f"scraped_song.txt", "r") as file:
          data = file.read()
          data_list = data.split("\n")
          data_list_iter = iter(data_list)
        for line in data_list_iter:
          if 'class="subItemText coloredLink"' in line:
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
            show_info.append(next(data_list_iter))
        for line in show_info:
          if "<" in line or "href" in line or "<b>" in line:
            show_info.remove(line)
        date = show_info[1]
        if "<" in date:
          date = "N/A"
        city = show_info[4]
        if "<" in city:
          city = "N/A"
        country = show_info[7]
        if "<" in country:
          country = "N/A"
        venue = show_info[10]
        if "<" in venue:
          venue = "N/A"
        type = show_info[13]
        if "<" in type:
          type = "N/A"
        tour = show_info[17]
        if "<" in tour:
          tour = "N/A"
        show_embed = discord.Embed(title=show_title, url=full_page, description=f"**Date:** {date} \n**City:** {city} \n**Country:** {country} \n**Venue:** {venue} \n**Type:** {type} \n**Tour:** {tour}")
        show_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
        show_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
        if "An error occurred" in page_text_str:
            await ctx.send("This release does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(embed=show_embed)

    @commands.command(brief="Sends merch info")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def merch(self, ctx, merch_id: str, info="no"):
      info = info.lower()
      check = 0
      template = "https://www.thebrpage.net/collectibles/item.asp?itemID="
      full_page = f"{template}{merch_id}"
      page_text = requests.get(full_page)
      page_text = BeautifulSoup(page_text.content, 'html.parser')
      soup_page = page_text.prettify()
      page_text_str = str(page_text)
      with open(f"scraped_merch.txt", "w") as file:
          file.write(str(soup_page))
      if info == "no":
          if "An error occurred" in page_text_str:
              await ctx.send("This piece of merch does not exist, or it does not have a page on the site.")
          else:
              await ctx.send(str(full_page))
      elif info in ['info', 'i']:
        merch_title = page_text.find('div', class_='pageTitle').text.strip()
        merch_info = []
        with open(f"scraped_merch.txt", "r") as file:
          data = file.read()
          data_list = data.split("\n")
          data_list_iter = iter(data_list)
        for line in data_list_iter:
          if '</colgroup>' in line:
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
            merch_info.append(next(data_list_iter))
        for line in merch_info:
          if "<td" in line or "</td" in line or "</tr":
            merch_info.remove(line)
        #HTML UNESCAPE DOESNT WORK FOR SOME REASON??
        merch_info[1] = merch_info[1].replace('&amp;', '&')
        merch_info[1] = merch_info[1].replace('&gt;', '>')
        if 'Posters, handbills & flags' in merch_info[1]:
          cate = merch_info[1]
          if "<" in cate:
            cate = "N/A"
          art = merch_info[3]
          if "<" in art:
            art = "N/A"
          year = merch_info[7]
          if "<" in year:
            year = "N/A"
          paper = merch_info[11]
          if "<" in paper:
            paper = "N/A"
          paper = merch_info[11]
          if "<" in paper:
            paper = "N/A"
          meas = merch_info[16]
          if "<" in meas:
            meas = "N/A"
          merch_embed = discord.Embed(title=merch_title, url=full_page, description=f"**Category:** {cate} \n**Artist:** {art} \n**Year:** {year} \n**Paper Quality:** {paper} \n**Measurements:** {meas}")
          merch_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
          merch_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
        else:
          cate = merch_info[1]
          if "<" in cate:
            cate = "N/A"
          color = merch_info[3]
          if "<" in color:
            color = "N/A"
          year = merch_info[7]
          if "<" in year:
            year = "N/A"
          auth = merch_info[11]
          if "<" in auth:
            auth = "N/A"
          manu = merch_info[-1]
          if "<" in manu:
            manu = "N/A"
          merch_embed = discord.Embed(title=merch_title, url=full_page, description=f"**Category:** {cate} \n**Color:** {color} \n**Year:** {year} \n**Authenticity:** {auth} \n**Manufacturer:** {manu}")
          merch_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
          merch_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
        if "An error occurred" in page_text_str:
            await ctx.send("This release does not exist, or it does not have a page on the site.")
        else:
            await ctx.send(embed=merch_embed)
  
    @commands.command(brief="Sends album tracklist")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def album(self, ctx, album_id: str, info="no"):
        tracks = []
        info = info.lower()
        template = "https://www.thebrpage.net/discography/item.asp?itemID="
        full_page = f"{template}{album_id}"
        page_text = requests.get(full_page)
        page_text = BeautifulSoup(page_text.content, 'html.parser')
        soup_page = page_text.prettify()
        page_text_str = str(page_text)
        with open(f"scraped_album.txt", "w") as file:
            file.write(str(soup_page))
        if info == "no":
            if "An error occurred" in page_text_str:
                await ctx.send("This album does not exist, or it does not have a page on the site.")
            else:
                await ctx.send(str(full_page))
        elif info == "info" or info == "i":
            with open(f"scraped_album.txt", "r") as file:
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
            album_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
            if "An error occurred" in page_text_str:
                await ctx.send("This song does not exist, or it does not have a page on the site.")
            else:
                await ctx.send(embed=album_embed)
            
    @commands.command(brief="Sends release info")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def release(self, ctx, release_id, info="no"):
        info = info.lower()
        template = "https://www.thebrpage.net/discography/variation.asp?varID="
        id = int(release_id)
        full_page = f"{template}{id}"
        page_text = requests.get(full_page)
        page_text = BeautifulSoup(page_text.content, 'html.parser')
        soup_page = page_text.prettify()
        page_text_str = str(page_text)
        with open(f"scraped_version.txt", "w") as file:
            file.write(str(soup_page))
        if info == "no":
            if "An error occurred" in page_text_str:
                await ctx.send("This release does not exist, or it does not have a page on the site.")
            else:
                await ctx.send(str(full_page))
        elif info == "info" or info == "i":
            release_info = []
            release_title = page_text.find('div', class_='pageTitle').text.strip()
            with open(f"scraped_version.txt", "r") as file:
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
            release_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
            if "An error occurred" in page_text_str:
                await ctx.send("This release does not exist, or it does not have a page on the site.")
            else:
                await ctx.send(embed=release_embed)
        
