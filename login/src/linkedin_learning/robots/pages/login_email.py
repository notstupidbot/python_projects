from robots.page import Page
from robots.form import Form
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class LoginEmailPage(Page):
    def __init__(self, page_name):
        super().__init__(page_name)
        self.form_selector="form#auth-id-form"
        self.form = Form(page_name, self.form_selector)
        self.form.setPage(self)

        self.form.setUrlSuccessPattern(r"uas/login\?session_key=")
        self.form.setUrlCheckPointPattern(r"checkpoint/challenge")

    def getForm(self):
        return self.form
    
    def guess(self, content):
        self.setContent(content)

        valid_page = False
        if self.content:
            formNd = self.hasForm()
            if len(formNd)>0:
                valid_page =  True
            else:
                log(lang("form_not_found_pquery",self.form_selector),"ND")
        return valid_page


login_email_page = LoginEmailPage('login_email_page')