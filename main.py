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
                if blg[2] != building_detection.BuildingStatus.BUILDING_NOT_FOUND:
                    pyautogui.moveTo(blg[2], blg[3], duration=1, tween=pyautogui.easeInOutQuad)
                    pyautogui.scroll(-1000)
                    pyautogui.moveRel(-100, 0, duration=0.5, tween=pyautogui.easeInOutQuad)
                    break
            screenshot_img = screenshotter.take_screenshot()
            buildings = building_detection.get_array_of_building_status(screenshot_img)

        for blg in reversed(buildings):
            if (blg[1] == building_detection.BuildingStatus.BUILDING_PURCHASABLE):
                pyautogui.moveTo(blg[2], blg[3], duration=1, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                break
        
        count = 0
        while count < 60:
            time.sleep(1)
            count += 1
            if keyboard.is_pressed('q'):
                break
    
if __name__ == "__main__":
    main()
    exit(0)
