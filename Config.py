from configparser import ConfigParser

class Config:

    def __init__(self):
        self.config = ConfigParser()
        self.token = None
        self.path = None
        self.client_id = None
        self.client_secret = None
        self.user_agent = None 
        self.posts_limit = None
        self.reload()
        
        
    def reload(self):
        self.config.read('E:/Python Workspace/Discord Bot/discord-meme-bot/config.ini')
        discord = self.config['discord']
        reddit = self.config['reddit']
        
        self.token = str(discord['token'])
        self.path = discord['path']
        self.client_id = reddit['client_id']
        self.client_secret = reddit['client_secret']
        self.user_agent = reddit  ['user_agent']
        self.posts_limit = reddit['posts_limit']
    
    def get_token(self):
        return self.token
        
    def get_path(self):
        return self.path
        
    def get_client_id(self):
        return self.client_id
        
    def get_client_secret(self):
        return self.client_secret
        
    def get_user_agent(self):
        return self.user_agent
        
    def get_posts_limit(self):
        return self.posts_limit