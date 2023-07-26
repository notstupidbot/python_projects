#!/usr/bin/env python3

from robots import Page, Human, JsonConfig
from robots.pages import unauthenticated_page,authenticated_page,login_email_page, login_passwd_page, login_pin_page, login_library_page, login_library_card_page
from robots.fn import log, lang, waitForCaptcha, inputAction
from robots.config import linkedin_learning_url
import login_individual
import login_library
import sys
from robots.datasource import DataSource
from api.course import fetchCourseUrl
######################################################
#JsonConfig
######################################################
json_config=JsonConfig(path="myconfig.json")
waitForCaptcha(json_config)
#######################################################
# Darabase settings
######################################################
db_setting_key="db_path"
db_path="my.db"
if not json_config.get(db_setting_key):
    json_config.set(db_setting_key, db_path)

ds = DataSource(db_path)
# sys.exit()
######################################################
# MIMIC HUMAN
######################################################
human = Human()
human.addPage(login_library_page).addPage(login_library_card_page).addPage(authenticated_page)
human.addPage(unauthenticated_page).addPage(login_email_page).addPage(login_passwd_page).addPage(login_pin_page)
######################################################
already_loged_in=False
# login_type="individual"
# login_type="library"
login_type = inputAction("library", human, json_config)
######################################################
# STEP 1 BROWSE THE LINKEDIN LEARNING WEBSITE
######################################################
# human try to browse linkedin learning website
content = human.browse(linkedin_learning_url, 'linkedin_learning_homepage')

# human try to guess page by name
if human.guessPage('unauthenticated_page',content):
    log(lang("you_are_not_login"),'info')

    if login_type == "individual":
        already_loged_in = login_individual.login(human, json_config)
    else:
        already_loged_in = login_library.login(human, json_config)

elif human.guessPage('authenticated_page',content):
    log(lang("you_are_loged_in"),'info')
    already_loged_in=True

# entry point after login process
if already_loged_in:
    log(lang('already_loged_in'))
else:
    human.clearCookies()
    # continue_next_step=True


