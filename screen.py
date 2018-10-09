import time
import datetime
import math
import image_processing
import session_log
import logic
import keyboard
import mouse
import determine_position
import current_stack
import introduction
import bar as metka

images_folder = "images/"
green_mark = [{'image_path':'green_board/green_mark.png', 'alias':'mark'}]
bar = [{'image_path':'bar/bar.png', 'alias':'bar'}]

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getScreenData():
        image_name = str(math.floor(time.time()))
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])
        if metka.seacrhBar(str(item['screen_area'])):
            image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
            last_row_action = session_log.getLastRowActionFromLogSession(str(item['screen_area']))
            if last_row_action in ['push', 'fold', 'end']:
                image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, item['screen_area'])
                hand = image_processing.searchCards(str(item['screen_area']), image_processing.getCards(), 4)
                determine_position.saveBlindImage(str(item['screen_area']), image_name, folder_name)
                current_stack.saveStackImage(str(item['screen_area']), image_name, folder_name)
                condition = session_log.checkConditionsBeforeInsert(hand, (item['screen_area']))
                if condition is not False:
                    logic.getDecision(item['screen_area'])
            elif last_row_action in ['open', 'call', 'check']:
                introduction.actionAfterOpen(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, str(item['screen_area']), last_row_action, image_name, folder_name)
            elif last_row_action == 'cbet':
                if introduction.checkIsFold(str(item['screen_area']), item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_name):
                    return
                keyboard.press('f')
                session_log.updateActionLogSession('fold', str(item['screen_area']))
            else:
                hand = session_log.getLastRowFromLogSession(str(item['screen_area']))
                if image_processing.checkCurrentHand(str(item['screen_area']), hand[0]['hand']):
                    logic.getDecision(item['screen_area'])
                else:
                    session_log.updateActionLogSession('end', str(item['screen_area']))