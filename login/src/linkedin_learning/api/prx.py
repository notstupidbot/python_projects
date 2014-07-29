from robots.fn import slugify,log,lang
from robots.human import Human
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir

import os
class Prx:
    def __init__(self, human=None):
        if not human:
            human=Human(cookie_path,browser_cache_dir)
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
        self.cache_path = '%s/%s-1.html' % (browser_cache_dir,self.page_name)
        # print(cache_path)
        if not no_cache:
            if os.path.exists(self.cache_path):
                log(lang('prx_loading_from_cache'))
                with open(self.cache_path, 'r') as file:
                    content = file.read()
                    return content
                
        return self.human.browse(url, self.page_name)