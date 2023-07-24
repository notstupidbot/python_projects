from robots.fn import log,lang,errors
from robots.config import linkedin_url, linkedin_learning_url


class LoginIndividual:
    def __init__(self, human):
        self.human=human
        self.linkedin_learning_login_url =""
        self.continue_next_step=False
        self.login_request_challenge=False
        self.next_url=""
        self.already_loged_in=False
    
    def alreadyLogedIn(self):
        return self.already_loged_in
    
    def getLoginUrl(self):
        unauth_page=self.human.getPage('unauthenticated_page')
        sign_in_btn=unauth_page.getSignInBtn()
        if sign_in_btn:
            self.linkedin_learning_login_url=sign_in_btn.attr('href')
            log(lang("login_url",self.linkedin_learning_login_url))
        else:
            errors(lang('could_not_find_login_url'),exit_progs=True)
        return self.linkedin_learning_login_url
    def start(self):
        account_setting={
            "email" : "sutoyocutexz@gmail.com",
            "password" : "Sejati86*#"
        }
        log(lang('using_account',"individual"))
        login_url=self.getLoginUrl()
        page_name='login_email_page'
        content=self.human.browse(login_url,page_name)
        if self.human.guessPage(page_name,content):
            current_page=self.human.getPage(page_name)
            formNd=current_page.hasForm()
            if formNd:
                form_action="%s%s" % (linkedin_url,formNd.attr('action'))
                current_form = current_page.getForm()
                if current_form:
                    current_form.setAction(form_action)
                    current_form.setPayload(current_page.getDoc())
                    current_form.setData('email', account_setting["email"])
                    content = current_form.post()
                    # log(content)
                else:
                    errors(lang('page_name_doesnt_have_form_object', page_name),exit_progs=True)
            pass
        else:
            errors(lang('cant_login_email_page'),exit_progs=True)


def login(human):
    
    li = LoginIndividual(human)
    li.start()
    return li.alreadyLogedIn()   

    
    