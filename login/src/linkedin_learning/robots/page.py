from robots.fn import pq

class Page:
    def __init__(self,name,guess_callback_fn=None):
        self.name=name
        self.doc=None
        self.content=""
        self.human=None
        self.guess_callback_fn=guess_callback_fn

    def setHuman(self, human):
        self.human = human    

    def getName(self):
        return self.name
    
    def setContent(self, content):
        self.content = content
        self.doc = pq(content)

    def setGuessCallback(self, callback):
        self.guess_callback_fn = callback
    
    # overide this for guessing method
    def guess(self,content):
        self.setContent(content)

        if self.guess_callback_fn:
            return self.guess_callback_fn(self)
        return False
    
    def findNode(self, selector, filter=None, startsWith=None):
        node = self.doc(selector)
        # print(self.doc)
        if node:
            if startsWith:
                return node.filter(lambda i: pq(this).text().startswith((startsWith)))
            elif filter:
                return node.filter(filter)
        return None
    def hasForm(self, form_name):
        return self.human.getForm(form_name).exists(self.doc)