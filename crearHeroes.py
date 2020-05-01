import pickle
import json
from heroesScrape import getHeroesBasicAttributes
from heroesScrape import getHeroesAdvancedAttributes
from calculoNiveles import calculosAttributesFaltantes
if __name__ == "__main__":
    
    heroesBasico_dict = getHeroesBasicAttributes('https://dota2.gamepedia.com/Table_of_hero_attributes')
    heroesCompleto_dict = getHeroesAdvancedAttributes('https://dota2.gamepedia.com/',heroesBasico_dict)
    heroesCompletoNiveles = calculosAttributesFaltantes(heroesCompleto_dict)

    with open('heroes.json', 'w') as fp:
        json.dump(heroesCompletoNiveles, fp)
        
    with open('heroes.pkl', 'wb') as f: #rb lee, wb escribe
            pickle.dump(heroesCompletoNiveles, f)

        # # with open('heroesCompleto.p', 'rb') as f:
        # #     heroes = pickle.load(f)
    