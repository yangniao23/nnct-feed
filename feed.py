#!/usr/bin/env python3
import requests
import re
import bs4
import lxml

url = r"http://www.nagaoka-ct.ac.jp"
get_url_info = requests.get(url)
bs4Obj = bs4.BeautifulSoup(get_url_info.text, 'lxml')

date = [tag.text for tag in bs4Obj.select("[class='feeds_date']")]
cat = [tag.text for tag in bs4Obj.select("[class='feeds_cat']")]
title = [tag.text for tag in bs4Obj.select("[class='feeds_title']")]
url = [tag.a.get('href') for tag in bs4Obj.select("[class='feeds_title']")]
news = [(s1, s2, s3, s4) for s1, s2, s3, s4 in zip(date, cat, title, url)]
print(news)
