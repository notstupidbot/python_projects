from robots.fn import log,lang,parseFormPayload,writeResp
class Form:
    def __init__(self,name, selector=None,filter=None):
        self.name = name
        self.data={}
        self.selector = selector
        self.selector_filter=filter
        self.action = ""
        self.browser=None
        self.human=None
        self.page=None
        self.last_resp=None
        pass
    
    def getLastResp(self):
        return self.last_resp
    def setPage(self, page):
        self.page=page
        self.human=page.getHuman()
    def getName(self):
        return self.name
    
    def setBrowser(self, browser):
        self.browser = browser
    
    def setHuman(self, human):
        if human:
            self.human = human
            self.browser = self.human.getBrowser()
    
    def setAction(self, action):
        self.action = action
    
    def setData(self, key_or_data, value=None):
        if type(key_or_data) is str:
            if value:
                self.data[key_or_data]=value
        else:        
            self.data = key_or_data
    
    def exists(self, doc):
        form = doc(self.selector)
        return form
    #set data based on current form input nodes
    def setPayload(self, doc):
        self.data= parseFormPayload(doc, self.selector) 

    def existsInContent(self, content):
        pass
    
    def post(self):
        log(lang('form_start_post',self.action))
        log(lang('form_post_payload',self.data))

        resp = self.browser.post(self.action, data=self.data)
        self.last_resp=resp

        log(lang('form_post_resp_code',resp.status_code))
        
        writeResp(resp, "%s_form" % (self.name), 1)
        return resp.text