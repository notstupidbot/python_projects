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

s = requests.Session()
s.headers.update({
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
})

resp = s.get('https://httpbin.org/headers')
print(resp.text)