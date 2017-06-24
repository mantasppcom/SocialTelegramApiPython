import json
import requests
import random


HYPERLINK_OF_STREAM = 'https://api.twitch.tv/kraken/streams/{0}'
HYPERLINK_OF_CHANNEL = 'https://api.twitch.tv/kraken/channels/{0}'
HYPERLINK_OF_VIDEO = 'https://api.twitch.tv/kraken/channels/{0}/videos?limit=10'


class Twitch:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.json_object_of_stream = json.loads(requests.get(HYPERLINK_OF_STREAM.format(self.channel_name)).text)
        self.json_object_of_channel = json.loads(requests.get(HYPERLINK_OF_CHANNEL.format(self.channel_name)).text)
        self.json_object_of_video =  json.loads(requests.get(HYPERLINK_OF_VIDEO.format(self.channel_name)).text)

    def get_video(self):
        random_number = random.randint(0, 9)
        url = str(self.json_object_of_video['videos'][0]['url'])
        random_url = str(self.json_object_of_video['videos'][random_number]['url'])
        return url, random_url

    def get_information(self):
        if self.json_object_of_stream['stream'] == None:
            status = 'offline'
            game = str(self.json_object_of_channel['game'])
            language = str(self.json_object_of_channel['language'])
            views = str(self.json_object_of_channel['views'])
            followers = str(self.json_object_of_channel['followers'])

            return url
            
        else:
            status = 'online'
            game = str(self.json_object_of_stream['stream']['game'])
            viewers = str(self.json_object_of_stream['stream']['viewers'])
            language = str(self.json_object_of_stream['stream']['channel']['broadcaster_language'])
            views = str(self.json_object_of_stream['stream']['channel']['views'])
            followers = str(self.json_object_of_stream['stream']['channel']['followers'])
            
            return status, game, language, views, followers, viewers
