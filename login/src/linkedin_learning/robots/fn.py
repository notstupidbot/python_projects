from pathlib import Path
from robots import config
from robots import langs
import re
import json
import requests
from pyquery import PyQuery as pquery
import sys
from datetime import datetime, timedelta
import time
import math
import html
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs



def timeAgo(seconds):
    current_time = datetime.now()
    time_ago = current_time - timedelta(seconds=seconds)

    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minutes"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hours"
    else:
        days = seconds // 86400
        return f"{days} days"

#get query string value from url
def getQueryStringValue(param_name,url):
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)
    return query_params.get(param_name, [''])[0]

def getCookiePath(cookie_name, cookie_jar):
    for cookie in cookie_jar:
        if cookie.name == cookie_name:
            return cookie.path

    return None
def log(str, t="log",verbose=False):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    log_type = t.lower()
    print_log=False
    log_color=CYAN
    if config.enable_loging:
        if log_type == "err":
            print_log = config.log_errors
            log_color=RED
        elif log_type == "info":
            print_log = config.log_info
            log_color=GREEN

        elif log_type == "nd":
            print_log = config.log_nd
            log_color=YELLOW

        else:
            print_log = True
        
        if verbose:
            print_log = print_log and config.log_verbose


    if print_log: 
        log_message= "[%s]%s" % (t.upper(),str)
        print(log_color + "[%s]%s" % (t.upper(),str) + RESET)

def errors(msg, exception=None, exit_progs=False,verbose=False):
    if exception:
        log(exception,'ERR',verbose=True)

    log(msg,'ERR',verbose=verbose)
    if exit_progs:
        sys.exit()

def validEmail(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Use the re.match function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

def inputAccountSettingIndividual(json_config):
    if not json_config.get("email"):
        json_config.set("email","you@gmail.com")
    if not json_config.get("password"):
        json_config.set("password","*******")
    
    print("Please Select Action:")

    print("1: Change Email")
    print("2: Change Password")
    print("p: Print")
    print("0: Back")

    user_choice = input("Enter your choice (1,2,0)[0]:" )
    choice = user_choice.lower()

    if choice == 'p':
        print("Email : %s" % json_config.get("email"))
        print("Password : %s" % json_config.get("password"))
        inputAccountSettingIndividual(json_config)
    
    if choice == '1':
        email = input("Enter email:" )
        if validEmail(email):
            json_config.set("email",email)
        else:
            errors(lang('is_not_valid_email',email))
        
        inputAccountSettingIndividual(json_config)

    if choice == '2':
        password = input("Enter password (min 4 char):" )
        if len(password)>=4:
            json_config.set("password",password)
        else:
            errors(lang('is_not_valid_password',password))
        
        inputAccountSettingIndividual(json_config)


    


def inputAccountSettingLibrary(json_config):
    if not json_config.get("library_id"):
        json_config.set("library_id","***")
    if not json_config.get("card_number"):
        json_config.set("card_number","*****")
    if not json_config.get("pin"):
        json_config.set("pin","*****")
    
    print("Please Select Action:")

    print("1: Change Library ID")
    print("2: Change Card Number")
    print("3: Change PIN")
    print("p: Print")

    print("0: Back")

    user_choice = input("Enter your choice (1,2,3,0)[0]:" )
    choice= user_choice.lower()
    if choice == 'p':
        print("Library ID : %s" % json_config.get("library_id"))
        print("Card Number : %s" % json_config.get("card_number"))
        print("PIN : %s" % json_config.get("pin"))
        inputAccountSettingLibrary(json_config)
    
    if choice == '1':
        library_id = input("Enter Library ID (min 2 chars):" )
        if len(library_id) >=2 :
            json_config.set("library_id",library_id)
        else:
            errors(lang('is_not_valid_library_id',library_id))
        
        inputAccountSettingLibrary(json_config)

    if choice == '2':
        card_number = input("Enter Card Number (min 4 char):" )
        if len(card_number)>=4:
            json_config.set("card_number",card_number)
        else:
            errors(lang('is_not_valid_card_number',card_number))
        
        inputAccountSettingLibrary(json_config)
    
    if choice == '3':
        pin = input("Enter PIN (min 4 char):" )
        if len(pin)>=4:
            json_config.set("pin",pin)
        else:
            errors(lang('is_not_valid_pin',pin))
        
        inputAccountSettingLibrary(json_config)
        


def inputAccountSetting(json_config):
    print("Please Select Login type:")

    print("1: Individual Account")
    print("2: Library Account")
    print("0: Back")
    user_choice = input("Enter your choice (1,2,0):" )
    choice = user_choice.lower()
    # Process the user's choice
    if choice == '1':
        inputAccountSettingIndividual(json_config)
    
    elif choice == '2':
        inputAccountSettingLibrary(json_config)
    
    elif choice == '0':
        pass
    else:
        inputAccountSetting(json_config)



def inputAction(default_login_type,human,json_config):
    print("Please Select Action:")

    print("1: Continue using Individual Account")
    print("2: Continue using Library Account")
    print("3: Clear Cookies (Logout)")
    print("4: Account Settings")
    print("0: Exit")

    login_type = default_login_type
    default_code=2
    
    user_choice = input("Enter your choice (1,2,3,4,0)[%i]:" % (default_code))
    choice = user_choice.lower()
    # Process the user's choice
    if choice == '1':
        login_type="individual"
    
    elif choice == '2':
        login_type="library"

    elif choice == '3':
        human.clearCookies()
        login_type=inputAction(login_type,human,json_config)

    elif choice== '4':
        inputAccountSetting(json_config)
        login_type=inputAction(login_type,human,json_config)

    elif choice== '0':
        sys.exit()

    else:
        login_type=choice

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

def waitForCaptcha(json_config, last_run_timeout_max=7):
    current_dt=datetime.now()
    if not json_config.get('last_run_timestamp'):
        json_config.set('last_run_timestamp', current_dt.timestamp())

    last_run_dt = datetime.fromtimestamp(json_config.get('last_run_timestamp'))
    last_run_rest = current_dt - last_run_dt
    last_run_timeout = math.ceil(last_run_rest.total_seconds())
    
    need_to_wait = last_run_timeout < last_run_timeout_max
    sleep_timeout = last_run_timeout_max - last_run_timeout

    if sleep_timeout < 0:
        sleep_timeout = 0
    
    need_to_wait_message= ""

    if need_to_wait:
        need_to_wait_message= "need to wait for %s second" % (sleep_timeout)

    print("Last run %s ago %s" %(timeAgo(last_run_timeout), need_to_wait_message))
    
    if need_to_wait:
        print("waiting for %s second " % (sleep_timeout))
        time.sleep(sleep_timeout)

    current_dt=datetime.now()
    json_config.set('last_run_timestamp',current_dt.timestamp())


# convert data to desired format
def convertData(src, c_type):
    if c_type == "unquote":
        return unquote(src)
    elif c_type == "unescape":
        return html.unescape(src)
    elif c_type == "dict" or c_type == "json.loads":
        return json.loads(src)
    return src
# get html meta data
def getMeta(name,doc,meta_config={}):
    selector="meta[name='%s']" % (name)
    metaNd=doc(selector)
    # print(metaNd)
    if len(metaNd) > 0:
        content = metaNd.attr("content")
        if name in meta_config:
            parser_type = meta_config[name]
            match_pipe=re.findall(r"\|",parser_type)
            if len(match_pipe)>0:
                parser_list = parser_type.split("|")
                for c_type in parser_list:
                    content = convertData(content, c_type)
            else:
                content=convertData(content, parser_type)
        return content    
    return None