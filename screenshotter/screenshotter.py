import pyautogui
import cv2 as cv
import os

__SCREENSHOT_FILE_NAME = "automated_screenshot.png"

def take_screenshot() -> cv.typing.MatLike:
    screenshot = pyautogui.screenshot()
    screenshot.save(__SCREENSHOT_FILE_NAME)
    screenshot = cv.imread(__SCREENSHOT_FILE_NAME, cv.IMREAD_COLOR)
    os.remove(__SCREENSHOT_FILE_NAME)
    assert screenshot is not None, "take_screenshot() -> screenshot is None"
    return screenshot
