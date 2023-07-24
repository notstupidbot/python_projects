#!/usr/bin/env python3

from robots import Page, Human, JsonConfig
from robots.pages import unauthenticated_page,login_email_page, login_passwd_page, login_pin_page
from robots.fn import log, lang, waitForCaptcha
from robots.config import linkedin_learning_url
import login_individual
import login_library
import sys

######################################################
#JsonConfig
######################################################
json_config=JsonConfig(path="myconfig.json")
waitForCaptcha(json_config)
# sys.exit()
######################################################
already_loged_in=False
login_type="individual"
######################################################
# MIMIC HUMAN
######################################################
human = Human()
human.addPage(unauthenticated_page).addPage(login_email_page).addPage(login_passwd_page).addPage(login_pin_page)
######################################################
# STEP 1 BROWSE THE LINKEDIN LEARNING WEBSITE
######################################################
# human try to browse linkedin learning website
content = human.browse(linkedin_learning_url, 'linkedin_learning_homepage')

# human try to guess page by name
if human.guessPage('unauthenticated_page',content):
    log(lang("you_are_not_login"),'info')

    if login_type == "individual":
        already_loged_in = login_individual.login(human)
    else:
        already_loged_in = login_library.login(human)
else:
    already_loged_in=True
# entry point after login process
if already_loged_in:
    log(lang('already_loged_in'))
else:
    human.clearCookies()
    # continue_next_step=True


