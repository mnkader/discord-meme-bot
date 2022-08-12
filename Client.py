import os
import discord
import traceback
import nest_asyncio
from discord.ext import commands
from RedditAsync import RedditAsync
from Config import Config
from ProfanityCheck import ProfanityCheck
import concurrent.futures
import time
nest_asyncio.apply()

class Client:
    def __init__(self):
        self.config = Config()
        self.profanity_check = ProfanityCheck('TODO', 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
        self.reddit_connections = {}
    
    def create_reddit_con(self, subreddit) -> RedditAsync:
        return RedditAsync(self.config, subreddit, self.profanity_check)

    def create_reddit_connections(self):
        my_list = ['ProgrammerHumor', 'memes']
        for x in range(len(my_list)):
            self.reddit_connections[my_list[x]] = self.create_reddit_con(my_list[x])
        return self.reddit_connections
    
    def get_token(self) -> str | None:
        return self.config.get_token()
    
    async def get_meme(self, connection : RedditAsync) -> list:
        return await connection.get_meme()
    
    def get_reddit_connection(self, subreddit : str) -> RedditAsync:
        return self.reddit_connections.get(subreddit)
    
    async def get_caption_and_image(self, subreddit : str) -> list:
        return await self.reddit_connections.get(subreddit).get_meme()  

client = Client()

TOKEN = client.get_token()

discord_bot = commands.Bot(command_prefix='!')

def refresh(connection : RedditAsync):
    connection.refresh()  

@discord_bot.event
async def on_connect():
    client.create_reddit_connections()
    my_list = ['ProgrammerHumor', 'memes']
    for x in range(len(my_list)):
        await client.get_reddit_connection(my_list[x]).refresh()
    print('on connect')


@discord_bot.event
async def on_ready():
        print(
            f'{discord_bot.user} is connected.\n'
        )

usage = '''```Usage: 
    !meme  : Sends a meme from the "ProgrammerHumor" Subreddit (SFW, Text-from-Image recognition might have a few gaps.).
    !info  : Returns a Usage Guide for this bot.
    !block list_of_words: A way to add profane words for future filtering, words to add is comma-delimited. e.g !block test,temp,tuna```'''

@discord_bot.command(name='block')
async def block(ctx : commands.context.Context):   
    message_content = ctx.message.content[:7]
    for word in message_content.split(','):
        client.profanity_check.add_bad_word(word) 

@discord_bot.command(name='info')
async def send_info(ctx):   
    await ctx.send(usage) 

@discord_bot.command(name='meme')
async def send_programming_meme(ctx):
    data = await client.get_caption_and_image('ProgrammerHumor')
    if data[0] != None and data[1] != None:
        await ctx.send(data[0]) #image caption
        await ctx.send(data[1])  #actual image
    else:
        await ctx.send('I find the lack of memes Disturbing...') #image caption
        await ctx.send('https://i.ytimg.com/vi/F1xAUfdK9FE/maxresdefault.jpg') #actual image
        await ctx.send('Please wait atleast 10 seconds before trying again.')
        await client.get_reddit_connection('ProgrammerHumor').refresh()

@discord_bot.command(name='funny')
async def send_normal_meme(ctx):
    data = await client.get_caption_and_image('memes')
    await ctx.send(data[0]) #image caption
    await ctx.send(data[1])  #actual image

if __name__ == '__main__':
    discord_bot.run(TOKEN)