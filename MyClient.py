import os
import discord
import nest_asyncio
from discord.ext import commands
from RedditScraper import RedditScraper
from Config import Config
from ProfanityCheck import ProfanityCheck

nest_asyncio.apply()

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix={"!"})
        self.config = Config()
        self.profanity_check = ProfanityCheck('TODO', 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
        self.token = self.config.get_token()

    def return_token(self):
        return self.token

    def create_reddit_con(self, subreddit):
        return RedditScraper(self.config.get_client_id(),self.config.get_client_secret(), self.config.get_user_agent(), subreddit, int(self.config.get_posts_limit()),self.profanity_check)
    
    async def on_connect(self):
        self.reddit_conn = self.create_reddit_con('ProgrammerHumor')
        self.reddit_memes = self.create_reddit_con('memes')
    
    async def on_ready(self):
        print(
            f'{client.user} is connected.\n'
        )
    
    async def help(self):
        help_string = '''Usage:\n !meme : To post a random programming meme to this chat. 
           \n !funny : To post a general meme to this chat (Currently in the testing phase, try it out, but beware...)
           \n !help : Opens up this Usage text.'''

    async def on_message(self, message):
        try:
            if message.content.startswith('!'):
                if "meme" in message.content:
                    await self.send_image(message, self.reddit_conn)
                if "funny" in message.content:
                    await self.send_image(message, self.reddit_memes)
                if "help" in message.content:
                    await self.help()
            if message.content.startswith('##'):
                self.profanity_check.add_bad_word(message.content[2:]) 
                print(self.profanity_check.contains_profanity(message.content[2:]))            
                await message.channel.send('I can\'t words today :( But I definitly won\'t be using that word again!')
        except:
            await message.channel.send('I find your lack of memes disturbing!')
            await message.channel.send('https://i.ytimg.com/vi/F1xAUfdK9FE/maxresdefault.jpg')

    async def send_image(self, message, connection):
        data = connection.get_meme()
        await message.channel.send(data[0]) #image caption
        await message.channel.send(data[1])  #actual image

client = MyClient()



@client.command(name='senddata')
async def send_data(ctx):
    await ctx.channel.send("hello there")
    
client.run(client.return_token())