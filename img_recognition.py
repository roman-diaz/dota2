import cv2
import numpy as np
import pickle
import os
from PIL import ImageGrab

def getImage():
    """
    Toma una imagen del dota y corta para la parte de los items
    """
    box = (776,669,917,740)
    im = ImageGrab.grab(box)
    im.save('imgs\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')
    return 'imgs\\full_snap__' + str(int(time.time())) +'.png'

def identificarItems(img_path,pathItems):
    # pathImgSlots = img_path.replace("/",C'\')
    itemSlots = cv2.imread(img_path)
    itemSlotsGrey = cv2.cvtColor(itemSlots,cv2.COLOR_BGR2GRAY)
    itemsSlotsGrey = cv2.pyrUp(itemSlotsGrey)
    items = []
    for itemImagen in pathItems:
        try:
            itemImgGrey = cv2.imread(itemImagen)
            # itemImgGrey = cv2.cvtColor(itemImg, cv2.COLOR_BGR2GRAY)          
            w,h = itemImgGrey.shape[::-1]
            res = cv2.matchTemplate(itemSlotsGrey, itemImgGrey, cv2.TM_CCOEFF_NORMED)
            threshhold = 0.7
            loc = np.where(res >= threshhold)
            for point in zip(*loc[::-1]):
                match = cv2.rectangle(itemSlotsGrey,point,(point[0]+w, point[1]+h), (0,255,255),2)
                if match.shape:
                    items.append(itemImagen.split('/')[-1].replace(".png",""))
                    break
        except Exception as e:
            pass
            # print(f"Error en {itemImagen.split('/')[-1]}")
            continue
    print(f"Items en la imagen: {items}")
    cv2.destroyAllWindows() 
    return items


    # cv2.imshow('detected',img_bgr)

    # cv2.waitKey(0)

if __name__ == "__main__":
    import time

    with open('pkl/itemsAttrIcons.p', 'rb') as handle:
        itemspkl = pickle.load(handle)
    pathIcons = "C:/Users/HP/Desktop/Python Scripts/Dota2/dota2/Icons/"

    # items = ['agiband','boots','tango']
    items = [rutaImg['icon'] for rutaImg in itemspkl.values()]
    pathItems = [pathIcons+x+'.png' for x in items]
    
    print("Items cargados...")
    for i in range(1,61):
        img = getImage()
        identificarItems(img,pathItems)
        time.sleep(60)
