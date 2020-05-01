from bs4 import BeautifulSoup
import urllib.request
import re
# import requests
from os.path  import basename
import pandas as pd

def getHeroesBasicAttributes(url):
    """Descarga info de dotawiki y genera un pickle con STR,AGI,INT base y ganancia x lvl"""
    dictHeroes = {}
    try:
        page = urllib.request.urlopen(url)
    except:
        print("An error occured.")
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('tbody')
    tr = table.findChildren("tr")
    tr = iter(tr)
    next(tr)
    next(tr)
    for filaHeroe in tr:
        td = filaHeroe.findChildren("td")
        td = list(td)
        dictHeroes[td[0].a['title']] = {
        'AtributoPrimario':td[1].a['title'],
        'Strength':{0:float(td[2].text.replace("\n","")),30:float(td[4].text.replace("\n","")),'Gain':float(td[3].text.replace("\n",""))},
        'Agility':{0:float(td[5].text.replace("\n","")),30:float(td[7].text.replace("\n","")),'Gain':float(td[6].text.replace("\n",""))},
        'Intelligence':{0:float(td[8].text.replace("\n","")),30:float(td[10].text.replace("\n","")),'Gain':float(td[9].text.replace("\n",""))}}
    return dictHeroes

def getHeroesAdvancedAttributes(url,heroesDict):
    for hero in heroesDict.keys():
        hero_url = hero.replace(" ","_")
        try:
            page = urllib.request.urlopen(url+hero_url)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find('table', attrs={'class':'evenrowsgray'}).tbody
            tr = table.findChildren("tr")
            tr = iter(tr)
            next(tr)
            for filaHeroe in tr:
                td = list(filaHeroe.findChildren("td"))
                atributo = filaHeroe.th.a['title'] 
                heroesDict[hero][atributo] = dict()
                if atributo == 'Attack damage':
                    heroesDict[hero][atributo][0] =td[0].text.replace("\n","").replace("\u2012","-")
                    heroesDict[hero][atributo][1] =td[1].text.replace("\n","").replace("\u2012","-")
                    heroesDict[hero][atributo]['Check'] =td[4].text.replace("\n","").replace("\u2012","-")
                else:
                    heroesDict[hero][atributo][0] = float(td[0].text.replace("\n",""))
                    heroesDict[hero][atributo][1] = float(td[1].text.replace("\n",""))
                    heroesDict[hero][atributo]['Check'] = float(td[4].text.replace("\n",""))

            table = soup.find('table', attrs={'class':'oddrowsgray'}).tbody
            tr = table.findChildren("tr")
            tr = iter(tr)

            for filaHeroe in tr:
                td = filaHeroe.find("td")
                atributo = filaHeroe.th.a['title'] 
                heroesDict[hero][atributo] = td.text.replace("\n","")
        except Exception as e:
            pass
    return heroesDict   

if __name__ == "__main__":
    import pickle
    import json
    dictHeroes = getHeroesBasicAttributes('https://dota2.gamepedia.com/Table_of_hero_attributes')
    dictHeroesCompleto = getHeroesAdvancedAttributes('https://dota2.gamepedia.com/',dictHeroes)

    with open('heroesCompleto.json', 'w') as fp:
        json.dump(dictHeroesCompleto, fp)

    




