import image_processing
import cv2
import numpy as np
import postgresql
import db_conf
import math
import time
import error_log
import datetime

#Поиск элемента, который говорит, что пришла очередь хода
def seacrhBar(screen_area):
    saveBarImage(screen_area, str(math.floor(time.time())), 'images/')
    path = image_processing.getLastScreen(getBarArea(str(screen_area)))
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('bar/bar.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if len(loc[0]) != 0:
        return True

    return False

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getBarArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select bar_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['bar_area']

def getBarData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data

def saveBarImage(screen_area, image_name, folder_name):
    try:
        folder_name = folder_name + str(datetime.datetime.now().date())
        for value in getBarData(str(getBarArea(str(screen_area)))):
            image_path = folder_name + "/" + str(getBarArea(str(screen_area))) + "/" + image_name + ".png"
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'], image_path, value['screen_area'])
    except Exception as e:
        error_log.errorLog('saveBlindImage', str(e))
        print(e)
