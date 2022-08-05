

import os
import discord
import nest_asyncio
from discord.ext import commands
from RedditScraper import RedditScraper
from Config import Config

nest_asyncio.apply()

class MyClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.token = self.config.get_token()
        self.path = self.config.get_path()
        
    def return_token(self):
        return self.token
        
    def create_reddit_con(self, subreddit):
        return RedditScraper(self.path,self.config.get_client_id(),self.config.get_client_secret(), self.config.get_user_agent(), subreddit, int(self.config.get_posts_limit()))
    
    async def on_connect(self):
        self.reddit_conn = self.create_reddit_con('ProgrammerHumor')
        self.reddit_memes = self.create_reddit_con('memes')
    
    async def on_ready(self):
        print(
            f'{client.user} is connected.\n'
        )
        
    async def on_message(self, message):
        if message.content.startswith('!'):
            if "meme" in message.content:
                await self.send_image(message, self.reddit_conn)
            if "aati" in message.content:
                await message.channel.send('https://youtu.be/AiIBKcd4m5Q?t=97')
            if "funny" in message.content:
                await self.send_image(message, self.reddit_memes)
        
    async def send_image(self, message, connection):
        data = connection.get_meme()
        filename = data[0][0] # actual file locaction
        with open(filename, 'rb') as fh:
            f = discord.File(fh, filename=filename)
        await message.channel.send(data[2]) #image caption
        await message.channel.send(file=f)  #actual image
client = MyClient()
client.run(client.return_token())