import os
import image_processing
import cv2
import math
import time
import datetime
import error_log
import db_query


def search_bar(screen_area, db):
    save_bar_image(screen_area, str(math.floor(time.time())), 'images/', db)
    path = db_query.get_last_screen(db_query.get_bar_area(screen_area, db), db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template_path = 'bar/red_mark.png'
    if image_processing.cv_data_template(template_path, img_rgb) > 0:
        return True
    blue_mark = 'bar/blue_mark.png'
    #if windows license expired
    if image_processing.cv_data_template(blue_mark, img_rgb) > 0:
        os.system("taskkill /im StarsCaption.exe")
        error_log.play_alarm_sound()
        error_log.error_log('bar', 'license expired')
        os.startfile('C:\\StarsCaption\\StarsCaption.exe')
    return False


def save_bar_image(screen_area, image_name, folder_name, db):
    try:
        folder_name = folder_name + str(datetime.datetime.now().date())
        for value in db_query.get_bar_data(db_query.get_bar_area(screen_area, db), db):
            image_path = folder_name + "/" + str(db_query.get_bar_area(str(screen_area), db)) + "/" + image_name + ".png"
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'],
                                     image_path, value['screen_area'], db)
    except Exception as e:
        error_log.error_log('red_mark', str(e))


def save_stack_image(screen_area, image_name, folder_name, db):
    try:
        for val in db_query.get_stack_data(db_query.get_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(db_query.get_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     str(val['screen_area']), db)
    except Exception as e:
        error_log.error_log('saveStackImage', str(e))
        print(e)