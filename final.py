import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])

import requests
import json

import re

from bs4 import BeautifulSoup

url = 'https://www.lawyered.in/legal-disrupt?categoryId='

result = {}
for i in range(6):
    if i != 2:
        res = requests.get(url + str(i+1))
        soup = BeautifulSoup(res.content, 'html.parser')
        articles = soup.find_all('div', attrs={'class':'small-post mb-5'})
        contents = {}
        for k, article in enumerate(articles):
            content = {}
            content['article_link'] = 'https://www.lawyered.in/' + article.h5.a.get('href')
            content['article_title'] = article.h5.text.strip()
            content['article_desc'] = article.p.text.strip()
            content['article_published_date'] = article.find_all('li')[0].text.strip()
            content['time_to_read'] = article.find_all('li')[1].text.strip()
            contents[k] = content
        title = soup.find_all('a', attrs={'href':'/legal-disrupt?categoryId=' + str(i+1)})[0].text.strip()
        result[title] = contents

with open("final.json", "w") as outfile:
    json.dump(result, outfile)
