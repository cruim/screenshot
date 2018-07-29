import image_processing
import logic
from PIL import Image, ImageGrab
import mouse
import cv2
import datetime
import math
import time
import numpy as np

images_folder = "images/"

#Поиск кнопки sitout
def searchSitoutButton(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('sitout_button/sitout_button.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

#Проверка, ушло ли окно в sitout
def checkIsSitout():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getUIButtonData("sitout_button"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchSitoutButton(str(item['screen_area'])) == 1:
            mouse.moveMouse(item['x_mouse'], item['y_mouse'])
            mouse.leftClick()
    logic.updateIterationTimer("sitout_button")