import requests
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

client = commands.Bot(command_prefix="!")

Roles = ["COD", "Garry's Mod", "GTA 5", "Valorant", "Apex", "League of Legends", "Fortnite", "SoT", "Among Us",
         "Rust", "PUBG", "Rainbow Six", "Phasmophobia", "Overwatch", "Warzone", "Krunker.io"]  # add your server roles here

# Replace with Discord Bot Token.
Token = 'ODQ5MjgzNzI2NTYyNDI2ODkw.YLY7Gw.eBGoN4XsHy0C192P95LZa8woC_E'


@client.event
async def on_ready():
    print("Bot has started running")
    await client.change_presence(activity=discord.Game(name="cmd: ++search"))


@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://gamingforecast.fun/wp-json/wp/v2/posts"
    complete_url = base_url + "?search=" + search_term
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n", color=0x349bfc)
    embed.set_author(name="Gaming Forecast")
    embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
    try:
        for count, value in enumerate(result):
            title = value["title"]["rendered"]
            url = value["link"]
            embed.description = embed.description + \
                f"{count + 1}. [{title}]({url})\n"
        embed.set_footer(text='This message will be deleted in 1 Hour.')

        await ctx.send(embed=embed, delete_after=3600.0)
    except:
        await ctx.send("There is something wrong with the response.")

client.recentPosts = None
client.recentPostsTime = None
client.recentPostsEdit = None


@tasks.loop(seconds=10.0)
async def fetchUpdates():
    url = "https://gamingforecast.fun/wp-json/wp/v2/posts"
    resp = requests.get(url)
    recheck = resp.json()
    # posts = blog.posts().list(blogId=BlogID).execute()
    postsList = recheck[0]["title"]["rendered"]
    if not client.recentPosts:
        client.recentPosts = postsList
        titleValue = str(postsList)
        urlValue = str(recheck[0]["link"])

        channel = client.get_channel(837621843929071669)  # Add channel ID
        embed = discord.Embed(title="New cheats available on the blog!",
                              description=f"[{titleValue}]({urlValue})")

        embed.set_author(name="Gaming Forecast")
        embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
        for i in Roles:
            if i.lower() in postsList.lower():
                guild = client.guilds[0]
                await channel.send(discord.utils.get(guild.roles, name=i).mention)
                await channel.send(embed=embed)
                break

        client.recentPosts = postsList

fetchUpdates.start()

client.run(Token, bot=True)
