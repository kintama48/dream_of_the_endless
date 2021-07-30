import json
import os
import platform
import random
import sys
import aiohttp
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    # shows the bot's information
    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        embed = discord.Embed(
            description="Dream of the Endless",
            color=0xD5059D
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="heisenbaig#8473",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.message.author}"
        )
        await context.send(embed=embed)

    # shows the server's information
    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    # ping a bot to check if it's alive or not
    @commands.command(name="ping")
    async def ping(self, context):
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xD5059D
        )
        await context.send(embed=embed)

    # get the invite link of the bot
    @commands.command(name="invite")
    async def invite(self, context):
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263).",
            color=0xD5059D
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    # get the invite link of the discord server of the bot
    @commands.command(name="server", aliases=["support", "supportserver"])
    async def server(self, context):
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/HzJ3Gfr).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    # @commands.command(name="poll")
    # async def poll(self, context, *, title):
    #     """
    #     Create a poll where members can vote.
    #     """
    #     embed = discord.Embed(
    #         title="A new poll has been created!",
    #         description=f"{title}",
    #         color=0x42F56C
    #     )
    #     embed.set_footer(
    #         text=f"Poll created by: {context.message.author} • React to vote!"
    #     )
    #     embed_message = await context.send(embed=embed)
    #     await embed_message.add_reaction("👍")
    #     await embed_message.add_reaction("👎")
    #     await embed_message.add_reaction("🤷")

    # @commands.command(name="8ball")
    # async def eight_ball(self, context, *, question):
    #     """
    #     Ask any question to the bot.
    #     """
    #     answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
    #                'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
    #                'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
    #                'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
    #                'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
    #     embed = discord.Embed(
    #         title="**My Answer:**",
    #         description=f"{answers[random.randint(0, len(answers))]}",
    #         color=0x42F56C
    #     )
    #     embed.set_footer(
    #         text=f"The question was: {question}"
    #     )
    #     await context.send(embed=embed)

    # check the current bitcoin price
    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":Information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0xD5059D
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
