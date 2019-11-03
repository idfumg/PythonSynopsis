#!/usr/bin/env python

import re, requests

request = requests.get("http://www.yandex.ru")
links = re.findall("<a href=(.*?)>.*?</a>", request.text)
[print(link) for link in links]
