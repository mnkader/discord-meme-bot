import praw
import re
import urllib.request

class RedditScraper:

    def __init__(self, path, client_id, client_secret, user_agent, subreddit, posts_limit, profanity_checker):
        self.profanity_check = profanity_checker
        self.posts_limit = posts_limit
        self.path = path
        self.image_urls = []
        self.image_captions = []
        self.image_types = ['jpg','jpeg','gif','png']
        self.pattern = None
        self.used_urls = []
        self.counter = 0
        self.local_images = []
        
        self.reddit = praw.Reddit(client_id = client_id, 
                     client_secret = client_secret, 
                     user_agent = user_agent)
        self.subreddit = self.reddit.subreddit(subreddit)     
        self.load_image_types()
        self.refresh() 

    #refreshes the posts then gets the new meme list, sets counter to 0
    def refresh(self):
        print('refreshing...')
        self.counter = 0 
        self.image_urls = []
        self.image_captions = [] 
        self.find_memes(self.posts_limit)

    def add_profanity(self, word):
        self.profanity_check.add_bad_word(word)

    def has_profanity(self, caption):
        return self.profanity_check.contains_profanity(caption)

    def filter_posts(self, posts):
        for post in posts:
            if(self.is_image(post) and not self.has_profanity(str(post.title))):
                self.image_urls.append(str(post.url))
                self.image_captions.append(str(post.title))
    
    #gets all posts self.post that have image links
    def find_memes(self, posts_limit):
        posts = self.subreddit.hot(limit=posts_limit-(posts_limit/2))
        self.filter_posts(posts)
        if(len(self.image_urls) < posts_limit):
            posts = self.subreddit.new(limit=(posts_limit-len(self.image_urls)))
            self.filter_posts(posts)  
    
    #returns true if the post url is an image link
    def is_image(self, post):
        return self.pattern.search(post.url) != None      

    #creates a pattern used to check if a url is an image link
    def load_image_types(self):
        self.pattern = re.compile('|'.join(r'\b{}\b'.format(type) for type in self.image_types))
    
    #True if url is used, False if it's not used
    def is_used_image(self, url):
        return url in self.used_urls
    
    #data[0]: image caption, data[1]: http url
    def get_meme(self):
        #checks if posts need to be refreshed
        if(self.counter >= len(self.image_urls)):
            self.refresh()
            
        data = self.get_image()
            
        #add downloaded image to used image urls list
        if(data[1] != None):
            self.used_urls.append(data[1])
        return data
    
    def get_image(self):
        for x in range(len(self.image_urls)):
            #if image is not used, return it
            if(not self.is_used_image(self.image_urls[x])):
                image_url = self.image_urls[x]
                image_caption = self.image_captions[x]
                return [image_caption,image_url]
        self.find_memes(self.posts_limit + 5)
        return self.get_image()