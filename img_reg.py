import cv2
import numpy as np
path = "C:/Users/HP/Desktop/Python Scripts/Dota2/dota2/"
# items = ['agiband','boots','tango']
items = ['agiband','boots','tango','power']
pathItems = [path+x+'.png' for x in items]

for itemImagen in pathItems:
    img_bgr = cv2.imread('prueba2.png')
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(itemImagen,0)
    w,h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshhold = 0.8
    loc = np.where(res >= threshhold)
    for point in zip(*loc[::-1]):
        match = cv2.rectangle(img_bgr,point,(point[0]+w, point[1]+h), (0,255,255),2)
        if match.shape:
            print(itemImagen)
            break
    # cv2.imshow('detected',img_bgr)

    # cv2.waitKey(0)

    cv2.destroyAllWindows() 