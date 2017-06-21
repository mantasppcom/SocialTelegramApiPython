import requests
import json
import random


VK_API = 'https://api.vk.com/method/{0}?{1}'


class VkApi:
    def __init__(self, domain, method_name):
        self.domain = domain
        self.method_name = method_name
        self.count = '10'

        if domain.startswith('-') == False:
            self.paramaters = 'domain={0}&count={1}'.format(
                self.domain,
                self.count
            )

        if domain.startswith('-'):
            self.paramaters = 'owner_id={0}&count={1}'.format(
                self.domain,
                self.count
            )

        self.json_object = requests.get(VK_API.format(
            self.method_name,
            self.paramaters
            )
        )

        self.response = self.json_object.json()['response']

    def generate_video_list(self):
        video_list = []
        vid = 0
        video_owner_id = 0

        for dict_response in self.response[1:]:
            attachments = dict_response['attachments'][0]
            if 'video' in attachments:
                video_owner_id = attachments['video']['owner_id']
                vid = attachments['video']['vid']
                video_list.append(vid)

        return video_list, video_owner_id

    def generate_photo_list(self):
        photos = []

        for dict_response in self.response[1:]:
            attachments = dict_response['attachments'][0]
            if 'photo' in attachments:
                link_of_photo = attachments['photo']['src_big']
                photos.append(link_of_photo)

        return photos

    def generate_gif_list(self):
        gifs = []

        for dict_response in self.response[1:]:
            attachments = dict_response['attachments'][0]
            if 'doc' in attachments:
                link_of_gif = attachments['doc']['url']
                gifs.append(link_of_gif)

        return gifs

    def generate_post_list(self):
        posts = []

        for dict_response in self.response[1:]:
            posts.append(dict_response['id'])
            owner_id = dict_response['from_id']

        return posts, owner_id


class VkRandom:
    def __init__(self, posts, video, photos, gifs):
        self.posts = posts
        self.video = video
        self.photos = photos
        self.gifs = gifs

    def random_post(self):
        if len(self.posts) > 0:
            random_number = random.randint(0, len(self.posts) - 1)
            return str(self.posts[random_number])

    def last_post(self):
        if len(self.posts) > 0:
            return str(self.posts[1])

    def random_video(self):
        if len(self.video) > 0:
            random_number = random.randint(0, len(self.video) - 1)
            return str(self.video[random_number])

    def random_photo(self):
        if len(self.photos) > 0:
            random_number = random.randint(0, len(self.photos) - 1)
            return str(self.photos[random_number])

    def random_gif(self):
        if len(self.gifs) > 0:
            random_number = random.randint(0, len(self.gifs) - 1)
            return str(self.gifs[random_number])

class VkLinks:
    def __init__(self, domain, group_id, post_id, video_owner_id, vid, last):
        self.domain = domain
        self.group_id = group_id
        self.post_id = post_id
        self.video_owner_id = video_owner_id
        self.vid = vid
        self.last = last

    def generate_link(self):
        if self.domain.startswith('-') == False and len(self.post_id) > 1:
            link = 'https://vk.com/{0}?w=wall{1}_{2}'.format(
                self.domain,
                str(self.group_id),
                str(self.post_id)
            )
            return str(link)

        else:
            return None
        if self.domain.startswith('-') and len(self.post_id) > 1:
            link = 'https://vk.com/club?{0}w=wall{1}_{2}'.format(
                self.domain[1:],
                str(self.group_id),
                str(self.post_id)
            )
            return str(link)

        else:
            return None

    def generate_last_link(self):
        if self.domain.startswith('-') == False and len(self.post_id) > 1:
            link = 'https://vk.com/{0}?w=wall{1}_{2}'.format(
                self.domain,
                str(self.group_id),
                str(self.last)
            )
            return str(link)

        else:
            return None
        if self.domain.startswith('-') and len(self.post_id) > 1:
            link = 'https://vk.com/club?{0}w=wall{1}_{2}'.format(
                self.domain[1:],
                str(self.group_id),
                str(self.last)
            )
            return str(link)

        else:
            return None

    def generate_video_link(self):
        if self.domain.startswith('-') == False and len(self.vid) > 1:
            if self.video_owner_id > 1:
                link = 'https://vk.com/{0}?z=video{1}_{2}'.format(
                    self.domain,
                    str(self.video_owner_id),
                    str(self.vid)
                )
                return str(link)

            else:
                return None

        else:
            return None

        if self.domain.startswith('-') and len(self.vid) > 1:
            if self.video_owner_id > 1:
                link = 'https://vk.com/club{0}?z=video{1}_{2}'.format(
                    self.domain[1:],
                    str(self.video_owner_id),
                    str(self.vid)
                )
                return str(link)

            else:
                return None
        else:
            return None


class GenerateElements:
    def __init__(self, post_link, video_link, photo_link, gif_link, last_link):
        self.post_link = post_link
        self.video_link = video_link
        self.photo_link = photo_link
        self.gif_link = gif_link
        self.last_link = last_link

    def generate_vk_post(self):
        return self.post_link

    def generate_vk_last_post(self):
        return self.last_link

    def generate_vk_video(self):
        return self.video_link

    def generate_vk_photo(self):
        return self.photo_link

    def generate_vk_gif(self):
        return self.gif_link


def vk_main(domain, method_name):
    vkapi = VkApi(domain, method_name)
    vkrandom = VkRandom(
        vkapi.generate_post_list()[0],
        vkapi.generate_video_list(),
        vkapi.generate_photo_list(),
        vkapi.generate_gif_list()
    )

    links = VkLinks(
        domain,
        vkapi.generate_post_list()[1],
        vkrandom.random_post(),
        vkapi.generate_video_list()[1],
        vkrandom.random_video(),
        vkrandom.last_post()
    )
    
    generate_elements = GenerateElements(
        links.generate_link(),
        links.generate_video_link(),
        vkrandom.random_photo(),
        vkrandom.random_gif(),
        links.generate_last_link()
    )
    return generate_elements
