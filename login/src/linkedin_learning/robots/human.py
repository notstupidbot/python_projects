from robots.browser import Browser
from robots.fn import log,lang,writeResp, clearCookies
import sys
class Human:
    def __init__(self):
        self.browser = Browser()
        self.pages = {} 
        self.forms = {} 
        self.browse_counts = {}
    
    def getBrowser(self):
        return self.browser
    
    def addPage(self, page):
        self.pages[page.getName()] = page
        page.setHuman(self)
        return self


    def addForm(self, form):
        self.form[form.getName()] = form
        form.setHuman(self)
        return self

    def getBrowseCount(self, page_name):
        if not page_name in self.browse_counts:
            self.browse_counts[page_name] = 0
        
        self.browse_counts[page_name] += 1

        return self.browse_counts[page_name]    
    def getPage(self,page_name):
        if not page_name in self.pages:
            log(lang('human_doesnt_have_page',page_name),'ERR')
            print(self.pages)
            sys.exit()
        
        return self.pages[page_name]

    def guessPage(self, page_name, content):
        return self.getPage(page_name).guess(content)
    
    def browse(self, url, page_name):
        log(lang('human_start_browsing',url))
        resp= self.browser.get(url)
        
        log(lang('human_browsing_resp_code',resp.status_code))
        writeResp(resp, page_name, self.getBrowseCount(page_name))
        return resp.text
        
        return None

    def getBrowser(self):
        return self.browser
        
    def fillForm(self,form_name, key, value):
        self.forms[form_name].setDataItem(key, value)

    def clearCookies(self):
        log(lang('human_clear_cookies'))
        clearCookies()

    
    
    
               