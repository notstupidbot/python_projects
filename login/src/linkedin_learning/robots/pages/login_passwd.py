from robots.page import Page
from robots.form import Form
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class LoginPasswdPage(Page):
    def __init__(self, page_name):
        super().__init__(self, page_name)
        self.form_selector="form#auth-id-form"

    def guess(self, content):
        self.setContent(content)

        valid_page = False
        if self.content:
            form = self.doc(self.form_selector)
            if len(form)>0:
                valid_page =  True
            else:
                log(lang("form_not_found_pquery",self.form_selector),"ND")
        return valid_page


login_passwd_page = LoginPasswdPage('login_passwd_page')