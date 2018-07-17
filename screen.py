from PIL import Image, ImageGrab
import time
import datetime
import math
import image_processing
import session_log

images_folder = "images/"

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    time.sleep(2)
    for item in image_processing.getScreenData():
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, str(item['screen_area']))

        # Если последняя строка для текущей области имеет статус отличный от null
        if image_processing.getLastScreen(str(item['screen_area']) is not None):
            hand = image_processing.searchPlayerHand(str(item['screen_area']))
            #Если рука обнаружена на скрине
            if hand != '':
                #Вставляем новую запись в session_log
                session_log.insertIntoLogSession(str(item['screen_area']), hand)

