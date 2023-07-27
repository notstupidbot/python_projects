from robots.fn import slugify,log,lang
from robots.human import Human

import os
class Prx:
    def __init__(self, human=None):
        if not human:
            human=Human()
        self.human = human
        self.page_name= ""
        self.cache_path= ""
    
    def getHuman(self):
        return self.human
    
    def getCachePath(self):
        return self.cache_path
    
    def getPageName(self):
        return self.page_name
    
    def get(self, url, no_cache=False):
        self.page_name=slugify(url.replace('/','-')).replace('https--wwwlinkedincom','ll')
        self.cache_path = 'html_cache/%s-1.html' % self.page_name
        # print(cache_path)
        if not no_cache:
            if os.path.exists(self.cache_path):
                log(lang('prx_loading_from_cache'))
                with open(self.cache_path, 'r') as file:
                    content = file.read()
                    return content
                
        return self.human.browse(url, self.page_name)