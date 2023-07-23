#!/usr/bin/env python3
"""
GET /cgi-bin/luci/;stok=2f69655b53a0411330da3221a5075166?status=1&_=0.11888017226259384 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: sysauth=2ea5a707924c8f4061f33551d7fff573; sysauth=
Host: 10.10.0.1
Referer: http://10.10.0.1/cgi-bin/luci
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36

"""
import requests
import http.cookiejar

def get_cookie_path(cookie_name, cookie_jar):
    for cookie in cookie_jar:
        if cookie.name == cookie_name:
            return cookie.path

    return None

s = requests.Session()
s.headers.update({
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
})

LOGIN_URL='http://10.10.0.1/cgi-bin/luci'
SECURE_URL='http://10.10.0.1'

resp = s.post(LOGIN_URL,data={'username':'root','password':'Sejati86*#'})

# resp = s.get('https://httpbin.org/cookies')
try:
    setCookie = resp.headers['Set-Cookie'].split(" ")
    # print(get_cookie_path('sysauth', resp.cookies))
    stok_path=setCookie[1].replace('path=','')
    SECURE_URL1 = "%s%s/admin/network/network" % (SECURE_URL,stok_path) 
    resp = s.get(SECURE_URL1)
    print(resp.text)


except Exception :
    pass
# print(resp.text)