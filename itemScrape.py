#FUNCIONANDO AL 100%
from bs4 import BeautifulSoup
import urllib.request
import re
import requests
from os.path  import basename
dictItems = {}
url = 'https://dota2.gamepedia.com'
try:
    page = urllib.request.urlopen(url+'/Items')
except:
    print("An error occured.")
soup = BeautifulSoup(page, 'html.parser')
divsItems = soup.find_all('div', attrs={'class': 'itemlist'})
for div in divsItems:
    itemsList = div.find_all('div')
    for item in itemsList:
        if item.a["href"].count("/") < 2:
            with open(basename(f'Icons/{item.a["href"][1:]}.png'), "wb") as f:
                f.write(requests.get(item.a.img["srcset"].split(" ")[0]).content)
            dictItems[item.a["href"]] = {'icon':item.a["href"][1:],'stats':[]} 

for item in dictItems.keys():
        try:
            page = urllib.request.urlopen(url+item)
            soup = BeautifulSoup(page, 'html.parser')
            res = soup.find_all(text=re.compile(r'^\+[0-9](.*)'))
            res = str(res[0].parent).split("<br/>")
            stats = [re.sub('<.*?>', '', attr) for attr in res ]
            stats.remove('\n')
            dictItems[item]['stats'] = stats
        except Exception as e:
            print(item+' no tiene')
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

with open('heroesWithIcons.p', 'wb') as fp:
    pickle.dump(dictItems, fp, protocol=pickle.HIGHEST_PROTOCOL)
