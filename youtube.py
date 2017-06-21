import variables
import json
import requests
import random


YOUTUBE_CHANNELS_LIST_ID = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={0}&maxResults=50&key={1}'
YOUTUBE_CHANNELS_LIST_USERNAME = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername={0}&maxResults=50&key={1}'
YOUTUBE_PLAYLISTITEMS_LIST = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={0}&key={1}'


class YoutubeApi:
    def __init__(self, key, username):
        self.key = key
        self.username = username

    def request(self):
        likes_items_list = []
        uploads_items_list = []
        likes = ''
        uploads = ''
        try:
            channels_list = json.loads(requests.get(YOUTUBE_CHANNELS_LIST_USERNAME.format(
                self.username,
                self.key)).text
            )['items'][0]['contentDetails']['relatedPlaylists']

        except IndexError:
            channels_list = json.loads(requests.get(YOUTUBE_CHANNELS_LIST_ID.format(
                self.username,
                self.key)).text
            )['items'][0]['contentDetails']['relatedPlaylists']

        if 'likes' in channels_list:
            likes = channels_list['likes']
            likes_items_list = json.loads(requests.get(YOUTUBE_PLAYLISTITEMS_LIST.format(
                likes,
                self.key)).text
            )

        if 'uploads' in channels_list:
            uploads = channels_list['uploads']
            uploads_items_list = json.loads(requests.get(YOUTUBE_PLAYLISTITEMS_LIST.format(
                uploads,
                self.key)).text
            )
            
        return likes_items_list, uploads_items_list


class GenerateLists:
    def __init__(self, likes_items_list, uploads_items_list):
        self.likes_items_list = likes_items_list
        self.uploads_items_list = uploads_items_list

    def generate_lists(self):
        uploads_video_id = []
        likes_video_id = []
        video_id = []
        if len(self.uploads_items_list) > 1:
            for item in self.uploads_items_list['items']:
                uploads_video_id.append(item['snippet']['resourceId']['videoId'])
            return uploads_video_id + likes_video_id
        if len(self.likes_items_list) > 1:
            for item in self.likes_items_list['items']:
                likes_video_id.append(item['snippet']['resourceId']['videoId'])
            return uploads_video_id + likes_video_id


class YoutubeVideo:
    def __init__(self, video_id):
        self.video_id = video_id

    def random(self):
        random_number = random.randint(0, len(self.video_id) - 1)
        random_video = self.video_id[random_number]
        return random_video

    def last(self):
        last_video = self.video_id[0]
        return last_video


class YoutubeLinks:
    def __init__(self, random, last):
        self.random = random
        self.last = last

    def generate_links(self):
        random_link = 'https://youtube.com/watch?v={0}'.format(str(self.random))
        last_link = 'https://youtube.com/watch?v={0}'.format(str(self.last))
        return random_link, last_link



def youtube_main(name):
    youtubeapi = YoutubeApi(variables.YOUTUBE_KEY, name)
    generate_lists = GenerateLists(youtubeapi.request()[0], youtubeapi.request()[1])
    youtube_video = YoutubeVideo(generate_lists.generate_lists())
    links = YoutubeLinks(youtube_video.random(), youtube_video.last())
    random_link = links.generate_links()[0]
    last_link = links.generate_links()[1]
    return random_link, last_link
