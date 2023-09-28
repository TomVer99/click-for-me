import pyautogui
import keyboard
import time

import building_detection.building_detection as building_detection
import screenshotter.screenshotter as screenshotter

__DEBUG = False
__MINIMUM_BUY_TIME = 10
__BUY_DECREASE_TIME = 15
__BUY_INCREASE_TIME = 60
__SCROLL_AMOUNT = 1000
__QUIT_KEY = 'q'

def main():
    count_upper = 60
    was_able_to_buy_previously = False

    while not keyboard.is_pressed(__QUIT_KEY):
        screenshot_img = screenshotter.take_screenshot()
        buildings = building_detection.get_array_of_building_status(screenshot_img)

        debug("Checking if we are at the bottom of the list of buildings")

        if buildings[len(buildings) - 1][1] == building_detection.BuildingStatus.BUILDING_NOT_FOUND:
            debug("We are not at the bottom of the list of buildings, scrolling down")
            for blg in buildings:
                if blg[1] != building_detection.BuildingStatus.BUILDING_NOT_FOUND:
                    move_to_and_scroll(-__SCROLL_AMOUNT, blg[2], blg[3])
                    break
            screenshot_img = screenshotter.take_screenshot()
            buildings = building_detection.get_array_of_building_status(screenshot_img)

        debug("Buying a building")

        bought_a_building = False
        for blg in reversed(buildings):
            if (blg[1] == building_detection.BuildingStatus.BUILDING_PURCHASABLE):
                move_to_and_click(blg[2], blg[3])
                bought_a_building = True
                break

        if not bought_a_building:
            debug("No building to buy, scrolling up to see if we can buy a building further up")
            for blg in reversed(buildings):
                if (blg[1] != building_detection.BuildingStatus.BUILDING_NOT_FOUND):
                    move_to_and_scroll(__SCROLL_AMOUNT, blg[2], blg[3])
                    break

            screenshot_img = screenshotter.take_screenshot()
            buildings = building_detection.get_array_of_building_status(screenshot_img)

            for blg in reversed(buildings):
                if (blg[1] == building_detection.BuildingStatus.BUILDING_PURCHASABLE):
                    move_to_and_click(blg[2], blg[3])
                    bought_a_building = True
                    break
            
            for blg in reversed(buildings):
                if (blg[1] != building_detection.BuildingStatus.BUILDING_NOT_FOUND):
                    move_to_and_scroll(-__SCROLL_AMOUNT, blg[2], blg[3])
                    break

        if not bought_a_building and not was_able_to_buy_previously:
            debug(f"No building was able to be bought twice in a row, increasing wait time to {count_upper}")
            count_upper += __BUY_INCREASE_TIME
        elif bought_a_building and was_able_to_buy_previously:
            debug(f"A building was able to be bought twice in a row, decreasing wait time to {count_upper}")
            count_upper -= __BUY_DECREASE_TIME
            if count_upper < __MINIMUM_BUY_TIME:
                count_upper = __MINIMUM_BUY_TIME

        was_able_to_buy_previously = bought_a_building

        debug(f"Waiting for {count_upper} seconds before checking again")
        
        count = 0
        while count < count_upper and not keyboard.is_pressed(__QUIT_KEY):
            time.sleep(1)
            count += 1
    
    pyautogui.alert('Cookie Clicker Bot has finished!')

def move_to_and_click(x, y):
    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.moveRel(-100, 0, duration=0.5, tween=pyautogui.easeInOutQuad)

def move_to_and_scroll(scroll, x, y):
    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.scroll(scroll)
    pyautogui.moveRel(-100, 0, duration=0.5, tween=pyautogui.easeInOutQuad)

def debug(msg):
    if __DEBUG == True:
        print(msg)

if __name__ == "__main__":
    main()
    exit(0)
