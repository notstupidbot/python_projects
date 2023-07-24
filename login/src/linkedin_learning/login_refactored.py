#!/usr/bin/env python3

from robots import Page, Human
from robots.pages import unauthenticated_page,login_email_page, login_passwd_page
from robots.fn import log, lang
from robots.config import linkedin_learning_url
import login_individual
import login_library

already_loged_in=False

login_type="individual"
######################################################
# MIMIC HUMAN
######################################################
human = Human()
human.addPage(unauthenticated_page).addPage(login_email_page).addPage(login_passwd_page)
print(login_email_page)

######################################################
# STEP 1 BROWSE THE LINKEDIN LEARNING WEBSITE
######################################################
# human try to browse linkedin learning website
content = human.browse(linkedin_learning_url, 'linkedin_learning_homepage')
# print(content)

# human try to guess page by name
if human.guessPage('unauthenticated_page',content):
    log(lang("you_are_not_login"),'info')

    if login_type == "individual":
        already_loged_in = login_individual.login(human)
    else:
        already_loged_in = login_library.login(human)

# entry point after login process
if already_loged_in:
    log(lang('already_loged_in'))
else:
    human.clearCookies()
    # continue_next_step=True


