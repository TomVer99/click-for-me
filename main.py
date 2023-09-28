import pyautogui
import keyboard
import time

import building_detection.building_detection as building_detection
import screenshotter.screenshotter as screenshotter


def main():
    while not keyboard.is_pressed('q'):
        screenshot_img = screenshotter.take_screenshot()
        buildings = building_detection.get_array_of_building_status(screenshot_img)

        if buildings[len(buildings) - 1][1] == building_detection.BuildingStatus.BUILDING_NOT_FOUND:
            for blg in buildings:
                # Move to the first building that is on screen so that the scroll works
                if blg[1] != building_detection.BuildingStatus.BUILDING_NOT_FOUND:
                    move_to_and_scroll(-1000, blg[2], blg[3])
                    break
            screenshot_img = screenshotter.take_screenshot()
            buildings = building_detection.get_array_of_building_status(screenshot_img)

        for blg in reversed(buildings):
            if (blg[1] == building_detection.BuildingStatus.BUILDING_PURCHASABLE):
                move_to_and_click(blg[2], blg[3])
                break
        
        count = 0
        while count < 60 and not keyboard.is_pressed('q'):
            time.sleep(1)
            count += 1

def move_to_and_click(x, y):
    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.moveRel(-100, 0, duration=0.5, tween=pyautogui.easeInOutQuad)

def move_to_and_scroll(scroll, x, y):
    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.scroll(scroll)
    pyautogui.moveRel(-100, 0, duration=0.5, tween=pyautogui.easeInOutQuad)

if __name__ == "__main__":
    main()
    exit(0)
