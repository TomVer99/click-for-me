import pyautogui
import cv2 as cv

def take_screenshot() -> cv.typing.MatLike:
    screenshot = pyautogui.screenshot()
    screenshot.save("automated_screenshot.png")
    screenshot = cv.imread("automated_screenshot.png", cv.IMREAD_COLOR)
    assert screenshot is not None, "take_screenshot() -> screenshot is None"
    return screenshot
