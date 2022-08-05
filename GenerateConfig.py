# python 3.x
from configparser import ConfigParser

config = ConfigParser()

config.add_section('discord')
config.set('discord', 'TOKEN', 'My Discord TOKEN')
config.set('discord', 'PATH', 'My Path')
config.add_section('reddit')
config.set('reddit', 'CLIENT_ID', 'CLIENT_ID')
config.set('reddit', 'CLIENT_SECRET', 'CLIENT_SECRET')
config.set('reddit', 'USER_AGENT', 'USER_AGENT')
config.set('reddit', 'POSTS_LIMIT', '10')

with open(file='config.ini', mode='w') as f:
    config.write(f)