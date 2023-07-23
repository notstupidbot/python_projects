class Form:
    def __init__(self,name, selector=None,filter=None):
        self.name = name
        self.data=None
        self.selector = selector
        self.selector_filter=filter
        self.action = ""
        self.browser=None
        pass
    
    def getName(self):
        return self.name
    
    def setBrowser(self, browser):
        self.browser = browser
    
    def setAction(self, action):
        self.action = action
    
    def setData(self, data):
        self.data = data

    def exists(self, doc):
        pass
    def existsInContent(self, content):
        pass
    def post(self):
        return self.browser.post(self.action, data=self.data)