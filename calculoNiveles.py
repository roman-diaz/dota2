def calculosAttributesFaltantes(heroesDict):
    for hero in heroesDict.keys():
        ataque = heroesDict[hero]["Attack damage"][0].split("-") # RANGO ATK EN NIVEL 0
        PromedioAtaque = [int(x) for x in ataque]
        heroesDict[hero]["BaseAttack"] = int((PromedioAtaque[0]+PromedioAtaque[1])/2)       
        heroesDict[hero]["Base Armor"] = heroesDict[hero]['Armor'][0]
        heroesDict[hero]["Main Armor"] = {}
        heroesDict[hero]["Dmg Mult"] = {}
        heroesDict[hero]["HP"] = {}
        heroesDict[hero]["EHP"] = {}
        for i in range(1,31):
            heroesDict[hero]["Main Armor"][i] =  round(heroesDict[hero]["Base Armor"] + 0.16*(heroesDict[hero]['Agility'][0] + heroesDict[hero]["Agility"]['Gain']*i),2)
            heroesDict[hero]["Dmg Mult"][i] = round(1 - ((0.052 * heroesDict[hero]["Main Armor"][i]) / (0.9 + 0.048 * abs(heroesDict[hero]["Main Armor"][i]))),2)
            heroesDict[hero]["HP"][i] =  round(200 + heroesDict[hero]["Strength"][0] + heroesDict[hero]["Strength"]['Gain']*i*20,2 )
            heroesDict[hero]["EHP"][i] = round(heroesDict[hero]["HP"][i]/heroesDict[hero]["Dmg Mult"][i] ,2)
       
    return heroesDict



    