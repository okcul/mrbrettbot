import discord
import random
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        print('Cog Unloaded')

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(brief="Sends bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! It took {round(self.bot.latency*1000)} ms to send this message!")

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command(brief="Basic 8ball command with shitposting")
    async def ball(self, ctx, *, question):
        possible_answers = ["No.", "Yes.", "Maybe.", "Possibly.", "Is the sky blue?", "I cannot say for sure.", "Why are you asking me that?", "I have no idea.", "Ask again later.", "Fuck no.", "You're one of those, aren't you?", "It is certain.", "Most likely.", "Outlook good.", "Outlook bad."]
        answer = random.choice(possible_answers)
        await ctx.send(f'The answer to your question "{question}"... {answer}')

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command(brief="Sends requested ID")
    async def id(self, ctx, user=None):
        if user == None:
            await ctx.send(f"Your ID is: {ctx.message.author.id}")
        else:
            checkuserid = int(ctx.message.content[6:-1])
            await ctx.send(f"Requested ID is: {checkuserid}")

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command(brief="Rates input")
    async def rate(self, ctx, *, input=None):
        num = random.randint(1, 10)
        if input == None:
            await ctx.send(f"You have been rated as {num}/10.")
        elif "<@" in input:
            userid = int(ctx.message.content[8:-1])
            userid = str(userid)
            await ctx.send(f"<@{userid}> has been rated as {num}/10.")
        else: 
            await ctx.send(f"{input} has been rated as {num}/10.")


async def setup(bot):
    await bot.add_cog(General(bot))
