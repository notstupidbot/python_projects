#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import data
import json
import http.cookiejar
# print(data.username)
# print(data.password)
# ss = requests.Session()
# # ss.cookies = http.cookiejar.FileCookieJar('cookies.txt')
# # ss.cookies.load(ignore_discard=True)
# # Load cookies from 'cookies.txt' file
# try:
#     session.cookies = requests.cookies.cookiejar_from_dict(requests.utils.dict_from_cookiejar(requests.cookies.RequestsCookieJar()), cookie_dict=json.load(open('cookies.txt')))
# except FileNotFoundError:
#     pass
headers = { "Referer": "http://10.10.0.1/cgi-bin/luci",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

import requests
import http.cookiejar
import json

def save_cookies_to_file(session, filename):
    with open(filename, 'w') as f:
        json.dump(session.cookies.get_dict(), f)

def load_cookies_from_file(session, filename):
    try:
        with open(filename, 'r') as f:
            cookies = json.load(f)
            session.cookies.update(cookies)
    except FileNotFoundError:
        pass

# Example usage
# url = 'https://example.com'
session = requests.Session()

# # Make a request to set some cookies in the session
# response = session.get(url)

# Save cookies to file
# save_cookies_to_file(session, 'cookies.json')

# Create a new session and load cookies from file
# new_session = requests.Session()
load_cookies_from_file(session, 'cookies.json')

# Make a request with the loaded cookies
# response = new_session.get(url)
# Do something with the response...
"""
fetch("http://10.10.0.1/cgi-bin/luci/;stok=2f69655b53a0411330da3221a5075166?status=1&_=0.9065707517840089", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "sysauth=2ea5a707924c8f4061f33551d7fff573; sysauth=",
    "Referer": "http://10.10.0.1/cgi-bin/luci",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "GET"
});
"""

LOGIN_URL='http://10.10.0.1/cgi-bin/luci'
SECURE_URL='http://10.10.0.1/cgi-bin/luci/;stok=2f69655b53a0411330da3221a5075166'

def Login_Dummy_web(username,password):
    

    ACCESS_DATA={
        'username':username,
        'password' :password
    }
    RESULT=session.post(LOGIN_URL,data=ACCESS_DATA,headers=headers)
    RESULT=session.get(SECURE_URL,headers=headers)
    save_cookies_to_file(session, 'cookies.json')

    # ss.cookies.save(ignore_discard=True)
    # CK=requests.utils.dict_from_cookiejar(RESULT.cookies)
    # print(json.dumps(CK))
    return RESULT.text
    # RESULT=requests.post(LOGIN_URL,data=ACCESS_DATA)
    # CK=requests.utils.dict_from_cookiejar(RESULT.cookies)
    # RESULT2=requests.post(SECURE_URL,cookies={"sysauth":"f9d3c672916b2d71fce54802d3233a38"})
    # print(json.dumps(CK))
    # return "%s" % (RESULT2.text)

print(Login_Dummy_web(data.username,data.password))



