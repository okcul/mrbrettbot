import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from requests import get
from urllib import parse
from re import sub, findall

async def setup(bot):
      await bot.add_cog(TheBRPage(bot))
  
class TheBRPage(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  def cog_unload(self):
      print('Cog Unloaded')

  async def get_images(self, list): # to be used with data_list split by linebreaks
    # gets image to be used as embed thumbnail
    for line in list: 
      if 'image_src' in line:
        base_link = line
        base_link = findall(r'"(.*?)"', base_link) # regex, finds everything within quotes per line
        for link in base_link:
          if 'image_src' not in link:
            final_link = link
        final_link = final_link.replace(' ', '%20') # makes link a usable link by making sure there are no spaces
    try:
      return final_link
    except UnboundLocalError: # checks if there isnt a link to return
      final_link = 'https://www.thebrpage.net/img/thebrpage_logo_large.jpg' # placeholder image, site logo
      return final_link


  
  @commands.group()
  async def show(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("I need something to do with the show. Use `(help show` for information on this command.")


  @commands.cooldown(1, 3, commands.BucketType.user)
  @show.command(brief="Returns link to a show given the ID", aliases=['link', 'l', 'url', 'u'])
  async def show_link(self, ctx, query):
    query = await self.search_command_setup(query) # converts spaces into '+'
    page_link = f'https://www.thebrpage.net/shows/show.asp?showID={query}' # combines query and template
    page_text = get(page_link) # requests module
    page_text = BeautifulSoup(page_text.content, 'html.parser') # parses the content into html form
    if "An error occurred" in str(page_text):
      query = query.replace("+", " ") # removes '+' for readability
      await ctx.send(f"Show not found. Make sure to input a valid numerical ID. Use '(search show {query}' if needed.")
    else:
      await ctx.send(f'{page_link}')

  @commands.cooldown(1, 5, commands.BucketType.user)
  @show.command(brief="Returns info about a show given the ID", aliases=['info', 'i'])
  async def show_info(self, ctx, query):
    query = await self.search_command_setup(query)
    page_template = "https://www.thebrpage.net/shows/show.asp?showID="
    page_link = f"{page_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    if "An error occurred" in str(page_text):
      await ctx.send("Song not found. Make sure to check your spelling.")
    else:
      with open("scraped_show.txt", "w") as file:
          file.write(str(page_text))
      with open("scraped_show.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n") # splits data into list separated by linebreaks
      
      show_title = page_text.find('div', {'class':"pageTitle"}).text.strip() # pulls show title from html
  
      show_info = []
      embed_info = []
      check = 1
      for info in page_text.find_all('td', {'class':"subItemText coloredLink"}):
        show_info.append(info)
        check += 1
        if check == 4: # only takes first three tables
          break
  
      show_info_sing = str(show_info[0]) # takes first table
      show_info_sing = show_info_sing.split("\n") # splits at linebreaks
      for line in show_info_sing:
        if '<b>' in line: # specific tag that surrounds the info we need on thebrpage
          embed_info.append(line)
  
      new_info = []
      for info in embed_info:
        info = info.replace("<b>", "") # replaces html tags
        info = info.replace("</b>", "")
        info = info.replace("\r", "")
        if "href" not in info and "img" not in info:
          new_info.append(info)

      final_info = []
      for info in new_info:
        info = sub('^.*: ', '', info) # removes everything before the ':'
        final_info.append(info)

      date = final_info[0]
      city = final_info[1]
      country = final_info[2]
      venue = final_info[3]
      type = final_info[4]
  
      show_embed = discord.Embed(title=show_title.title(), url=page_link, description=f"**Date:** {date} \n**City:** {city} \n**Country:** {country} \n**Venue:** {venue} \n**Type:** {type}")
      show_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      show_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
      await ctx.send(embed=show_embed)



  
  @commands.group()
  async def release(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("I need something to do with the release. Use '(help release' for information on this command")

  @commands.cooldown(1, 3, commands.BucketType.user)
  @release.command(brief="Returns link to a release given its ID", aliases=['link', 'l', 'url', 'u'])
  async def release_link(self, ctx, query):
    query = await self.search_command_setup(query)
    page_link = f'https://www.thebrpage.net/discography/variation.asp?varID={query}'
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    if "An error occurred" in str(page_text): # checks if page is valid
      await ctx.send("Release not found. Make sure to check your spelling.")
    else:
      await ctx.send(f'{page_link}')

  @commands.cooldown(1, 3, commands.BucketType.user)
  @release.command(brief="Returns song info", aliases=['info', 'i'])
  async def release_info(self, ctx, query):
    query = await self.search_command_setup(query)
    page_template = "https://www.thebrpage.net/discography/variation.asp?varID="
    page_link = f"{page_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    if "An error occurred" in str(page_text): # checks if page is valid
      await ctx.send("Release not found. Make sure to check your spelling.")
    else:
      with open("scraped_release.txt", "w") as file:
          file.write(str(page_text))
      with open("scraped_release.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
      
      release_title = page_text.find('div', {'class':"pageTitle"}).text.strip() # pulls release title from html
  
      release_info = []
      embed_info = []
      check = 1
      for info in page_text.find_all('table', {'class':"flat fixedLayout"}):
        release_info.append(info)
        check += 1
        if check == 4: # only takes first three tables
          break
  
      release_info_sing = str(release_info[0]) # uses first table
  
      release_info_sing = release_info_sing.split("\n") # splits table by line breaks
      for line in release_info_sing:
        if '<td>' in line:
          embed_info.append(line)
        if 'Cover:' and 'Vinyl:' in line:
          embed_info.append(line)
  
      new_info = []
      for info in embed_info:
        info = info.replace("<td>", "") # removes html tags
        info = info.replace("</td>", "")
        info = info.replace("\r", "") # idk random shit that appears
        info = info.replace("\t", "")
        if "''" not in info:
          new_info.append(info)

      label = new_info[0]
      date = new_info[1]
      country = new_info[2]
      if 'CD' in new_info[4]:
        format = new_info[4]
        details = 'N/A'
      else:
        details = new_info[4]
        format = new_info[5]
      
      
      release_embed = discord.Embed(title=release_title, url=page_link, description=f"**Label:** {label} \n**Release Date:** {date} \n**Country:** {country} \n**Disc/Label Details:** {details} \n**Format:** {format}")
      release_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      release_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
      await ctx.send(embed=release_embed)

  
  
  @commands.group()
  async def song(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("I need something to do with the song. Use `(help song` for information on this command.")


  @commands.cooldown(1, 3, commands.BucketType.user)
  @song.command(brief="Returns link to a song", aliases=['link', 'l', 'url', 'u'])
  async def song_link(self, ctx, query):
    query = await self.search_command_setup(query)
    page_link = f'https://www.thebrpage.net/discography/song.asp?songName={query}'
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    if "An error occurred" in str(page_text): # checks if page is valid
      await ctx.send("Song not found. Make sure to check your spelling.")
    else:
      await ctx.send(f'{page_link}')


  @commands.cooldown(1, 5, commands.BucketType.user)
  @song.command(brief="Returns list of releases a song is on", aliases=['r', 'versions', 'v'])
  async def releases(self, ctx, query):
    query = await self.search_command_setup(query)
    page_template = "https://www.thebrpage.net/discography/song.asp?songName="
    link_template = "https://www.thebrpage.net/discography/"
    page_link = f"{page_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    if "An error occurred" in str(page_text):
      await ctx.send("Song not found. Make sure to check your spelling.") # checks if page is valid
    else:
      links = []
      filtered_links = []
      extra_filtered_links = []
      result_links = []
  
      for link in page_text.findAll('a'): # finds links based on html tag
        links.append(link.get('href'))
        
      for link in links:
        if link != None:  # removes empty links
          filtered_links.append(link)
  
      for link in filtered_links:
        if "discography" in link or "varID" in link:
          extra_filtered_links.append(link)
      
      for link in extra_filtered_links:
        if "img" not in link and "catID" not in link and "user" not in link and "contributors" not in link and "songs.asp" not in link and ".." not in link and "song.asp" not in link:
          result_links.append(link)

      result_links.remove(result_links[0]) # removes first element in list, as it will always be the song of the day
      await self.search_embed_setup(ctx, "version", query, result_links, link_template, page_link)


  @commands.cooldown(1, 3, commands.BucketType.user)
  @song.command(brief="Returns song info", aliases=['i'])
  async def song_info(self, ctx, query):
    query = await self.search_command_setup(query)
    page_template = "https://www.thebrpage.net/discography/song.asp?songName="
    page_link = f"{page_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    if "An error occurred" in str(page_text): # checks if page is valid
      await ctx.send("Song not found. Make sure to check your spelling.")
    else:
      with open("scraped_song.txt", "w") as file:
          file.write(str(page_text))
      with open("scraped_song.txt", "r") as file:
            data = file.read()
            data_list = data.split("\n")
      
      song_title = page_text.find('div', {'class':"pageTitle"}).text.strip() # pulls song title from html
  
      song_info = []
      embed_info = []
      check = 1
      for info in page_text.find_all('table', {'class':"flat fixedLayout"}):
        song_info.append(info)
        check += 1
        if check == 4: # only takes first three tables
          break
  
      song_info_sing = str(song_info[0]) # uses first table
  
      song_info_sing = song_info_sing.split("\n") # splits table by line breaks
      for line in song_info_sing:
        if '<td>' in line:
          embed_info.append(line)
  
      new_info = []
      for info in embed_info:
        info = info.replace("<td>", "") # removes html tags
        info = info.replace("</td>", "")
        new_info.append(info)
      
      author = new_info[0]
      release_date = new_info[1]
      try:
        bpm = new_info[2]
      except:
        bpm = "N/A"
  
      song_embed = discord.Embed(title=song_title.title(), url=page_link, description=f"**Written by:** {author} \n**Release Date:** {release_date} \n**BPM:** {bpm}")
      song_embed.set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      song_embed.set_thumbnail(url=f'{await self.get_images(data_list)}')
      await ctx.send(embed=song_embed)
    

  
  
  @commands.group()
  async def album(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("I need something to do with the album. Use `(help album` for information on this command.")

  @commands.cooldown(1, 3, commands.BucketType.user)
  @album.command(brief="Returns an album link given an ID", aliases=['url', 'link', 'u', 'l'])
  async def album_link(self, ctx, query):
    page_link = f'https://www.thebrpage.net/discography/item.asp?itemID={query}'
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')
    if "An error occurred" in str(page_text): # checks if page is valid
      await ctx.send("Song not found. Make sure to check your spelling.")
    else:
      await ctx.send(f'{page_link}')

  
  @commands.cooldown(1, 5, commands.BucketType.user)
  @album.command(brief="Returns an album tracklist given an ID", aliases=['tracklist', 'tr', 't', 'songs' 's'])
  async def album_tracklist(self, ctx, query):
    await ctx.send("placeholder command")
    # album tracklist within specific tags
    # scrape tracks and their names
    # generate links to tracks
    # set up embed


  @commands.cooldown(1, 5, commands.BucketType.user)
  @album.command(brief="Returns the releases of an album given an ID", aliases=['releases', 'r', 'versions', 'v'])
  async def album_releases(self, ctx, query):
    query = await self.search_command_setup(query)
    page_link_template = "https://www.thebrpage.net/discography/item.asp?itemID="
    page_template = "https://www.thebrpage.net/discography/"
    page_link = f"{page_link_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    album_name = page_text.find('div', {'class':"pageTitle"}).text.strip() # pulls title from html

    links = []
    filtered_links = []
    extra_filtered_links = []
    result_links = []

    for link in page_text.findAll('a'): # finds all links
      links.append(link.get('href')) # takes href attribute
      
    for link in links:
      if link != None:  # removes empty links
        filtered_links.append(link)

    for link in filtered_links:
      if "discography" in link or "varID" in link:
        extra_filtered_links.append(link)
    
    for link in extra_filtered_links:
      if "img" not in link and "catID" not in link and "user" not in link and "contributors" not in link and "songs.asp" not in link and ".." not in link:
          result_links.append(link)  

    result_links.pop(0) # removes first two, will always be discography page and song of the day
    result_links.pop(0)
    
    await self.search_embed_setup(ctx, "a_version", query, result_links, page_template, page_link, album_name)


  
  async def search_command_setup(self, old_query):
    query = parse.quote_plus(old_query) # replaces invalid characters
    query = query.replace('"', "") # same
    query = query.lower() # lowercase for readability
    return query

  async def search_embed_setup(self, ctx, type, query, links, link_template, url, album_name="x"):
    # album_name only used when finding album releases
    self.bot.num = 0
    link_num = 1
    category = ""
    link_dict = { # sets up dict for 'dynamic' variables in for loop
      'link_str0' : '',
      'link_str1' : '',
      'link_str2' : '',
      'link_str3' : '',
      'link_str4' : ''
    }
    match type:
      case 'release':
        category = "Releases"
      case 'show':
        category = "Shows"
      case 'merch':
        category = "Merch"
      case 'version':
        category = f"{query.title()}"
        
    for link in links:
      if link_num == 51: # breaks when over 50 links
        break
      link_dict[f'link_str{self.bot.num}'] += f"{link_num}: {link_template}{link}" # dynamic 'variables' (dict keys)
      link_dict[f'link_str{self.bot.num}'] += "\n" # adds line break
      link_num += 1
      if link_num in [11, 21, 31, 41, 51]:
        self.bot.num += 1 # increases page number

    self.bot.pages = {}
    for number in range(5): # sets up variable to be equal to dict key we need...
      nested_description = f'link_str{number}'
      
      if type == 'version': # song versions
        self.bot.pages[f'search_embed{number}'] = discord.Embed(title=f'Releases featuring "{category}"', url=url, description=f"{link_dict[f'{nested_description}']}") #... because f strings are weird when you try to nest them, so we need to condense them to only 2 layers

      elif type == 'a_version': # album versions
        album_name = album_name.title()
        self.bot.pages[f'search_embed{number}'] = discord.Embed(title=f'Releases of {album_name}', url=url, description=f"{link_dict[f'{nested_description}']}")
      
      else: # all other searches (merch, release, show)
        query = query.replace("+", " ")
        self.bot.pages[f'search_embed{number}'] = discord.Embed(title=f'Search results for "{query}" in {category}', url=url, description=f"{link_dict[f'{nested_description}']}")
        
      self.bot.pages[f'search_embed{number}'].set_footer(text="Created by ANAL#3547 || Requested by {}".format(ctx.author.name))
      
    self.bot.search_embed_message = await ctx.send(embed=self.bot.pages['search_embed0'], view=SearchView(self.bot))
    self.bot.num = 0 # creates attribute to send values to view


  
  
  @commands.group()
  async def search(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("I need something to search. Use `(help search` for information on this command.")

  @commands.cooldown(1, 5, commands.BucketType.user)
  @search.command(brief="Searches for merch", aliases=['m'])
  async def merch(self, ctx, query):
    query = await self.search_command_setup(query)
    search_template = "https://www.thebrpage.net/collectibles/search.asp?search="
    page_template = "https://www.thebrpage.net/collectibles/"
    page_link = f"{search_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    links = []
    filtered_links = []
    extra_filtered_links = []
    result_links = []

    for link in page_text.findAll('a'): # finds all links via html tag
      links.append(link.get('href'))
      
    for link in links:
      if link != None: # removes empty links
        filtered_links.append(link)

    for link in filtered_links:
      if "item.asp" in link: # filters in needed links
        extra_filtered_links.append(link)
    
    for link in extra_filtered_links:
      if "img" not in link and "catID" not in link and "user" not in link and "contributors" not in link and "songs.asp" not in link and ".." not in link: # filters out non-needed links
          result_links.append(link)  

    await self.search_embed_setup(ctx, "merch", query, result_links, page_template, page_link)

  
  @commands.cooldown(1, 5, commands.BucketType.user)
  @search.command(brief="Searches for shows", aliases=['show', 'sh'])
  async def show_search(self, ctx, query):
    query = await self.search_command_setup(query)
    search_template = "https://www.thebrpage.net/shows/search_shows.asp?search="
    page_template = "https://www.thebrpage.net/shows/"
    page_link = f"{search_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    links = []
    filtered_links = []
    extra_filtered_links = []
    result_links = []

    for link in page_text.findAll('a'): # finds links through html tag
      try:
        if "attend" not in link.get('title') and "added" not in link.get('title'): # filters out false positive links
          links.append(link.get('href'))
      except TypeError: # in case link has no title
        links.append(link.get('href'))
      
    for link in links:
      if link != None: # removes empty links
        filtered_links.append(link)

    for link in filtered_links:
      if "showID" in link:
        extra_filtered_links.append(link)
    
    for link in extra_filtered_links:
      if "#comments" not in link:
        result_links.append(link)  

    await self.search_embed_setup(ctx, "show", query, result_links, page_template, page_link)
  
  
  @commands.cooldown(1, 5, commands.BucketType.user)
  @search.command(brief="Searches for releases", aliases=['song', 's', 'r', 'release'])
  async def release_search(self, ctx, query):
    query = await self.search_command_setup(query)
    search_template = "https://www.thebrpage.net/discography/search.asp?search="
    page_template = "https://www.thebrpage.net/discography/"
    page_link = f"{search_template}{query}"
    page_text = get(page_link)
    page_text = BeautifulSoup(page_text.content, 'html.parser')

    links = []
    filtered_links = []
    extra_filtered_links = []
    result_links = []

    for link in page_text.findAll('a'): # finds all links based on html tag
      links.append(link.get('href'))
      
    for link in links:
      if link != None:  # removes empty links
        filtered_links.append(link)

    for link in filtered_links:
      if "discography" in link or "varID" in link:
        extra_filtered_links.append(link)
    
    for link in extra_filtered_links:
      if "img" not in link and "catID" not in link and "user" not in link and "contributors" not in link and "songs.asp" not in link and ".." not in link:
          result_links.append(link)  

    result_links.pop(0)
    result_links.pop(0)

    await self.search_embed_setup(ctx, "release", query, result_links, page_template, page_link)
    
    



class SearchView(discord.ui.View):
  def __init__(self, bot):
    super().__init__(timeout=60)
    self.bot = bot
    
  @discord.ui.button(label="First", emoji="⏪", style=discord.ButtonStyle.blurple)
  async def first(self, interaction, button):
    await self.bot.search_embed_message.edit(view=self, embed=self.bot.pages['search_embed0']) # sends to first page
    self.bot.num = 0
    await interaction.response.defer() # makes sure it doesnt say interaction failed


  @discord.ui.button(label="Previous", emoji="⬅️", style=discord.ButtonStyle.blurple)
  async def previous(self, interaction, button):
    self.bot.num -= 1 # sends to previous page
    if self.bot.num < 0: # checks if invalid number
      self.bot.num = 0
    await self.bot.search_embed_message.edit(view=self, embed=self.bot.pages[f'search_embed{self.bot.num}'])
    await interaction.response.defer() # makes sure it doesnt say interaction failed


  @discord.ui.button(label="Next", emoji="➡️", style=discord.ButtonStyle.blurple)
  async def next(self, interaction, button):
    self.bot.num += 1 # sends to next page
    if self.bot.num > 4: # checks if invalid number
      self.bot.num = 4
    await self.bot.search_embed_message.edit(view=self, embed=self.bot.pages[f'search_embed{self.bot.num}'])
    await interaction.response.defer() # makes sure it doesnt say interaction failed
    

  @discord.ui.button(label="Last", emoji="⏩", style=discord.ButtonStyle.blurple)
  async def last(self, interaction, button):
    await self.bot.search_embed_message.edit(view=self, embed=self.bot.pages['search_embed4']) # sends to last page
    self.bot.num = 4
    await interaction.response.defer() # makes sure it doesnt say interaction failed
