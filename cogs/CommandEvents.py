from datetime import datetime
from disnake import errors
from disnake.ext import commands
import time, disnake, os

channelID = int(os.getenv('LOGGING_CHANNEL_ID'))



class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded')
 
    @commands.Cog.listener()
    async def on_error(self, ctx, errors):
        print(ctx.command.name + "has failed!")
        print(errors)
        await ctx.send(f'eror hapen\nnfo:\n{errors}')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " success")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after)} seconds.')
        else:
            print(error)
            await ctx.send(f'An unknown error has occured\n\n{error}')

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        time = datetime.now().strftime('%H:%M:%S')
        embed = disnake.Embed(title="{} deleted a message".format(message.author.name),
                            description="", color=0xFF0000)
        embed.add_field(name=f"Message deleted in {message.channel}", value=message.content,
                        inline=True)
        embed.set_footer(text=f'ID: {message.id} • Time: {time}')
        channel = self.bot.get_channel(channelID)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if before.author == self.bot.user:
            return
        if before.content == after.content:
            return
        time = datetime.now().strftime('%H:%M:%S')
        embed = disnake.Embed(title=f"{before.author.name} edited a message",
                          description="", color=0xFF0000)
        embed.add_field(name=before.content, value="Before",
                        inline=True)
        embed.add_field(name=after.content, value="After",
                        inline=True)
        embed.set_footer(text=f'ID: {after.id} • Time: {time}')
        channel = self.bot.get_channel(channelID)
        await channel.send(embed=embed)


def setup(bot): 
    bot.add_cog(CommandEvents(bot))