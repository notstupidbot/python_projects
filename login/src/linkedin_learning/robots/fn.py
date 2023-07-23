from pathlib import Path
from robots import config
from robots import langs
import re
import json
import requests
from pyquery import PyQuery as pquery
import sys

def getCookiePath(cookie_name, cookie_jar):
    for cookie in cookie_jar:
        if cookie.name == cookie_name:
            return cookie.path

    return None
def log(str, t="log",verbose=False):
    log_type = t.lower()
    print_log=False
    if config.enable_loging:
        if log_type == "err":
            print_log = config.log_errors
        elif log_type == "info":
            print_log = config.log_info
        elif log_type == "nd":
            print_log = config.log_nd
        else:
            print_log = True
        
        if verbose:
            print_log = print_log and config.log_verbose


    if print_log:    
        print("[%s]%s" % (t.upper(),str))

def errors(msg, exception, exit_progs=False,verbose=False):
    if exception:
        log(exception,'ERR',verbose=True)

    log(msg,'ERR',verbose=verbose)
    if exit_progs:
        sys.exit()

def inputLoginType(defaultValue="individual"):
    print("Please Select Login type:")

    print("1: Individual Account")
    print("2: Library Account")
    login_type = defaultValue
    defaultCode=2
    if defaultValue=="individual":
        defaultCode=1
    user_choice = input("Enter your choice (1,2)[%i]:" % (defaultCode))
    # Process the user's choice
    if user_choice.lower() == '1':
        # login_type="individual"
        pass
    elif user_choice.lower() == '2':
        login_type="library"
    else:
        # print("Invalid choice. exit")
        # sys.exit()
        pass
    return login_type

def parseFormPayload(doc, form_selector):
    inputs = doc.find("%s input" % (form_selector))
    # print(inputs)
    payload={}
    for input in inputs:
        # print(input.value)
        payload[input.name]=input.value
    return payload 

def lang(key, data=None):
    global langs
    global config

    config_lang  = getattr(config,"lang")
    selected_langs = getattr(langs,config_lang)
    if hasattr(selected_langs, key):
        str = getattr(selected_langs, key)
        if not data:
            return str
        else:
            return str % (data)
    return key
def writeFile(path,content,mode="w"):
    try:
        with open(path, mode) as file:
            file.write(content)
            log(lang("write_file_success",path),verbose=True)

        return True
    except Exception as exception:
        errors(lang("could_not_write_file",path),exception,verbose=True)
        return False    

def writeResp(resp, page_name, index):
    global config
    if config.write_resp_text:
        path = "%s-%s.html" % (page_name, index)
        path = "html_cache/%s" % (path)
        writeFile(path,resp.text.replace('</head>','<title>%s</title></head>' % (resp.url)))

def matchUrl(pattern, url):
    matches = re.findall(pattern, url)
    return len(matches) > 0

def saveCookies(session, path="cookies.json"):
    try:
        cookies = requests.utils.dict_from_cookiejar(session.cookies)  # turn cookiejar into dict
        Path(path).write_text(json.dumps(cookies))  
        return True  
    except Exception as exception:
        errors(lang("could_not_write_cookie_file", path),exception)
        return False
def clearCookies(path="cookies.json"):
    try:
        cookies = {}
        Path(path).write_text(json.dumps(cookies))  
        return True  
    except Exception as exception:
        errors(lang("could_not_clear_cookie_file", path),exception)
        return False
    
def loadCookies(session, path="cookies.json"):
    try:
        cookies = json.loads(Path(path).read_text())  # save them to file as JSON
        cookies = requests.utils.cookiejar_from_dict(cookies)  # turn dict to cookiejar
        session.cookies.update(cookies)  # load cookiejar to current session
        return True
    except Exception as exception:
       errors(lang("could_not_load_cookie_file", path),exception) 
       return False
    
def dummyFn(a=None):
    log(lang('pquery_dummy_fn_called'))
    return None
def pq(html):
    pq_obj=None
    # log(html)
    if html == None:
        log(lang('pquery_called_with_empty_html'))
    else:
        try:
            pq_obj=pquery(html)
        except Exception as exception:
            errors(lang("pquery_error", path),exception) 
            pq_obj = dummyFn
    return pq_obj