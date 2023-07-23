from robots.fn import log,lang,errors
from robots.config import linkedin_url, linkedin_learning_url

def login(human):
    linkedin_learning_login_url=""
    continue_next_step = False
    next_url = ""
    last_resp=""
    login_request_challenge=False

    log(lang('using_account',"individual"))
    unauthenticated_page=human.getPage('unauthenticated_page')
    pass