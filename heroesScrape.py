from bs4 import BeautifulSoup
import urllib.request
import re
import requests
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
                    heroesDict[hero][atributo][0] =td[0].text.replace("\n","")
                    heroesDict[hero][atributo][1] =td[1].text.replace("\n","")
                    heroesDict[hero][atributo][30] =td[4].text.replace("\n","")
                else:
                    heroesDict[hero][atributo][0] = float(td[0].text.replace("\n",""))
                    heroesDict[hero][atributo][1] = float(td[1].text.replace("\n",""))
                    heroesDict[hero][atributo][30] = float(td[4].text.replace("\n",""))

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

def calculosAttributesFaltantes(heroesDict):

    for hero in heroesDict.keys():
        ataque = heroesDict[hero]["Attack damage"][0].split("‒")
        PromedioAtaque = [int(x) for x in ataque]
        heroesDict[hero]["BaseAttack"] = int((PromedioAtaque[0]+PromedioAtaque[1])/2)
        hero_df = pd.DataFrame(index=["BASE ARMOR","MAIN ARMOR","DAMAGE MULT","HP","DMG","DMGx4","EHP","DMGtoH"],columns=[x for x in range(1,30)])
    #     # ARMOR
        hero_df.loc["BASE ARMOR",:] = heroesDict[hero]['Armor'][0]
        hero_df.loc["MAIN ARMOR",1] = hero_df.loc["BASE ARMOR",1] + (heroesDict[hero]["Agility"][0]*0.16)
        hero_df.loc["DAMAGE MULT",1] = 1 - ((0.052 * hero_df.loc["MAIN ARMOR",1]) / (0.9 + 0.048 * abs(hero_df.loc["MAIN ARMOR",1])))
    #     #HP
        hero_df.loc["HP",1] = 200 + heroesDict[hero]["Strength"][0]*20 
        #ATK
        primary = heroesDict[hero]["AtributoPrimario"]
        for col in hero_df.columns:
            if col == 1:
                pass
            else:
           
                hero_df.loc["MAIN ARMOR",col] = (heroesDict[hero]["Agility"]['Gain']*0.16) + hero_df.loc["MAIN ARMOR",col-1]
                hero_df.loc["DAMAGE MULT",col] = 1 - ((0.052 * hero_df.loc["MAIN ARMOR",col]) / (0.9 + 0.048 * abs(hero_df.loc["MAIN ARMOR",col])))
                hero_df.loc["HP",col] =  heroesDict[hero]["Strength"]['Gain']*20 + hero_df.loc["HP",col-1]
            hero_df.loc["DMG",col] = (heroesDict[hero]["BaseAttack"] + heroesDict[hero][primary]["Gain"]*col) #FALTARIA AGREGARLE DAMAGE MULT DEL ENEMIGO AL Q LE PEGA 
            # hero_df.loc["DMGtoH",col] = (heroesDict[hero]["BaseAttack"] + heroesDict[hero][primary]["Gain"]*col)*hero_df[hero_actual].loc["DAMAGE MULT",col]

            # hero_df.loc["DMGx4",col] = hero_df.loc["DMG",col]*heroesDict[hero]["Attack speed"]/4
        heroesDict[hero]['Niveles'] = hero_df
    return heroesDict
if __name__ == "__main__":
    try:
        import cPickle as pickle
    except ImportError:  # python 3.x
        import pickle
    dictHeroes = getHeroesBasicAttributes('https://dota2.gamepedia.com/Table_of_hero_attributes')
    dictHeroesCompleto = getHeroesAdvancedAttributes('https://dota2.gamepedia.com/',dictHeroes)
    heroesCompleto = calculosAttributesFaltantes(dictHeroesCompleto)
    with open('heroesCompleto.p', 'wb') as f: #rb lee, wb escribe
        pickle.dump(heroesCompleto, f, protocol=pickle.HIGHEST_PROTOCOL)
    
   

    # with open('heroesCompleto.p', 'rb') as f:
    #     heroes = pickle.load(f)

    



