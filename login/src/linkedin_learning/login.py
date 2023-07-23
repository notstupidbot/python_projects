#!/usr/bin/env python3

import requests
import http.cookiejar
import sys
import re
import config
import langs
import state

from fn import clearCookies, pq, writeResp, lang, parseFormPayload, inputLoginType, inputLoginType, log, getCookiePath, matchUrl
import browser as browse

session = requests.Session()
browser = browse.Browser(session, config)

state.login_type = inputLoginType("library")
log(lang("using_account",state.login_type))

linkedin_url = "https://www.linkedin.com"
linkedin_learning_url='%s/learning' % (linkedin_url)
linkedin_learning_login_url=""
continue_next_step = False
next_url = ""
last_resp=""
login_request_challenge=False

log(lang("checking_login_credential"))

try:
    resp=browser.get(linkedin_learning_url)
    doc = pq(resp.text)
    last_resp=resp

    sign_in_btn = doc("a").filter(lambda i: pq(this).text().startswith(('Sign in')))
    if sign_in_btn:
        log(lang("sign_in_btn_not_found"),'nd')
        log(lang("you_are_not_login"),'info')

        linkedin_learning_login_url=sign_in_btn.attr('href')
        log(lang("login_url",linkedin_learning_login_url))
        continue_next_step = True
    else:
        state.is_loged_in = True
        writeResp(resp,200)

except Exception :
    log(Exception.getMessage(),"ERR")
    pass

login_step_index = 0

if continue_next_step:
    continue_next_step = False
    if not state.is_loged_in:
        log(lang("fetching_login_page"))
        resp=browser.get(linkedin_learning_login_url)
        last_resp=resp
        doc = pq(resp.text)
        login_step_index += 1 
        writeResp(resp,login_step_index)


        if state.login_type == "library":
            library_anchor_link=doc("a.signin__library")
            if library_anchor_link:
                linkedin_learning_login_url=library_anchor_link.attr("href")
                log(lang("login_url",linkedin_learning_login_url))
                resp=browser.get(linkedin_learning_login_url)
                last_resp=resp
                doc = pq(resp.text)
                login_step_index += 1
                writeResp(resp,login_step_index)
                form_selector="#library-tenant-form"
                form=doc(form_selector)
                if form:
                    next_url = resp.url
                    payload = parseFormPayload(doc, form_selector)
                    payload["tenantId"] = state.library["id"]

                    log(lang("next_url",next_url))
                    log(lang("next_post_payload"))
                    log(payload)
                    log(lang("send_library_id_post"))
                    login_step_index += 1
                    resp=browser.post(next_url, data=payload,allow_redirects=True)
                    writeResp(resp, login_step_index)

                    last_resp=resp
                else:
                    log(lang("form_not_found_pquery",form_selector),"ND")
                pass
        else:
        # elif state.login_type == "individual":
            form_id = "form#auth-id-form"
            form=doc(form_id)
            if form:
                next_url="%s%s" % (linkedin_url,form.attr('action'))
                payload= parseFormPayload(doc, form_id)
                payload["email"] = state.login["email"]

                log(lang("next_url",next_url))
                log(lang("next_post_payload"))
                log(payload)
                log(lang("send_email_login_post"))
                resp=browser.post(next_url, data=payload,allow_redirects=True)
                login_step_index += 1
                writeResp(resp,login_step_index)

                log(resp.url)
                
                url_success_pattern = r"uas/login\?session_key="
                
                if not matchUrl(url_success_pattern, resp.url):
                    print(lang("cant_continue_with_provided_email",payload["email"]))
                    sys.exit()

                continue_next_step = True
                last_resp=resp
            else:
                log(lang("form_not_found_pquery",form_id),"ND")

if continue_next_step:
    continue_next_step = False
    if not state.is_loged_in:
        log(lang("continue_login_page"))
        if state.login_type == "individual":
            doc = pq(last_resp.text)
            form_selector = "form.login__form"
            form=doc(form_selector)
            if form:
                
                next_url="%s%s" % (linkedin_url,form.attr('action'))
                
                payload = parseFormPayload(doc, form_selector)
                payload["session_password"] = state.login["password"]

                log(lang("next_url",next_url))
                log(lang("next_post_payload"))
                log(payload)
                log(lang("send_passwd_login_post"))

                resp=browser.post(next_url, data=payload,allow_redirects=True)
                login_step_index += 1
                writeResp(resp,login_step_index)
                
                url_checkpoint_pattern = r"checkpoint/lg/login-submit"
                if matchUrl(url_checkpoint_pattern, resp.url):
                     log(lang("cant_continue_with_provided_passwd",payload['session_password']))
                     sys.exit()
                url_checkpoint_challenge_pattern = r"checkpoint/challenge"
                if matchUrl(url_checkpoint_challenge_pattern, resp.url):
                     log(lang("login_requested_challenge"))
                     log(lang("please_open_device_to_get_pin_code"))
                     login_request_challenge = True
                
                continue_next_step = True
                last_resp = resp
                log(resp.url)
            else:
                log(lang("form_not_found_pquery",form_selector),"ND")

if continue_next_step:
    continue_next_step = False
    if not state.is_loged_in:
        log('Continue login page')
        if state.login_type == "individual":
            doc = pq(last_resp.text)
            
            if login_request_challenge:
                login_request_challenge = False
                verification_code = input(lang("enter_pin_code"))
                form_selector = "form.pin-verification-form"
                form=doc(form_selector)
                if form:
                    next_url="%s%s" % (linkedin_url,form.attr('action'))

                    payload=parseFormPayload(doc, form_selector)
                    payload["pin"]=verification_code
                    
                    log(lang("next_url",next_url))
                    log(lang("next_post_payload"))
                    log(payload)
                    log(lang("send_pin_login_post"))
                    
                    resp=browser.post(next_url, data=payload,allow_redirects=True)
                    login_step_index += 1
                    writeResp(resp,login_step_index)

                    log(resp.url)

                    url_check_add_phone_pattern=r"check/add-phone"
                    if matchUrl(url_check_add_phone_pattern, resp.url):
                        log(lang("login_requested_add_phone"))
                        log(lang("please_fix_this_problem_by_with_your_browser"))
                        log(lang("cant_continue_util_setup_complete"))
                        sys.exit()
                    url_success_pattern = r"www\.linkedin\.com/learning"
                    if matchUrl(url_success_pattern, resp.url):
                        log(lang("login_successful"))
                        state.is_loged_in=True
                        sys.exit()
                else:
                    log( lang("form_not_found_pquery",form_selector), "ND")


if state.is_loged_in:
    log("Hello World","info")
else:
    clearCookies()

