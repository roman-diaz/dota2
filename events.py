import os
from watchdog.events import RegexMatchingEventHandler
import time
from img_recognition import identificarItems
from creardictheroes import crearDfsEnemigos
class ImagesEventHandler(RegexMatchingEventHandler):

    IMAGES_REGEX = [r".*png$"]

    def __init__(self):
        super().__init__(self.IMAGES_REGEX)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}.png"
        time.sleep(5)
        items,itemspkl = identificarItems(filename)
        # print(f"Pkl tiene: {itemspkl}")
        for item in items:
            try:
                item = '/'+item
                print(f"{item} agrega {itemspkl[item]['stats']}")
            except:
                print(f"{item} no encontrado en pkl.")
        
        enemigos = ["crystal_maiden","lion","sniper","pudge","tusk"]
        hero_actual = "pudge"
        print(enemigos)
        print(f"jugando con {hero_actual}")

        dictHeroes = crearDfsEnemigos(hero_actual,enemigos)
        print(dictHeroes[hero_actual][5])

