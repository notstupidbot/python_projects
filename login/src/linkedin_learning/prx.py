from robots.browser import Browser
from robots.fn import slugify,log,lang
import os
class Prx:
    def __init__(self, human):
        self.human = human
    def getHuman(self):
        return self.human
    def get(self, url):
        page_name=slugify(url).replace('httpswwwlinkedincomlearning','ll-')
        cache_path = 'html_cache/%s-1.html' % page_name
        # print(cache_path)
        if os.path.exists(cache_path):
            print(lang('loading_from_cache'))
            with open(cache_path, 'r') as file:
                content = file.read()
                return content
        else:    
            return self.human.browse(url, page_name)