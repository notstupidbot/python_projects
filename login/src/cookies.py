#!/usr/bin/env python3

import requests

URL='https://httpbin.org/cookies'
CK={'location':'New York'}
response=requests.get(URL,cookies=CK)
print(response.text)