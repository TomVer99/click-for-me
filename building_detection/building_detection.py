import cv2 as cv
import numpy as np
import enum
import inspect

__IMAGE_PATH = "building_detection/"
__THRESHOLD = 0.9
__MAX_COLOR_DELTA = 10

class BuildingStatus(enum.Enum):
    BUILDING_NOT_FOUND = 0
    BUILDING_NOT_PURCHASABLE = 1
    BUILDING_PURCHASABLE = 2

def get_cursor_status(screenshot_img:cv.typing.MatLike) -> [int, int, int]:
    can_buy_img     = cv.imread(__IMAGE_PATH + "cursor_buy.png", cv.IMREAD_COLOR)
    can_not_buy_img = cv.imread(__IMAGE_PATH + "cursor_no_buy.png", cv.IMREAD_COLOR)
    return detect_building(screenshot_img, can_buy_img, can_not_buy_img)

def detect_building(screenshot_img:cv.typing.MatLike, can_buy_img:cv.typing.MatLike, can_not_buy_img:cv.typing.MatLike
                    , threshold:float = __THRESHOLD, max_color_delta:int = __MAX_COLOR_DELTA) -> [int, int, int]:
    assert screenshot_img  is not None, f"{inspect.stack()[1][3]}() -> screenshot_img is None"
    assert can_buy_img     is not None, f"{inspect.stack()[1][3]}() -> building_can_buy is None"
    assert can_not_buy_img is not None, f"{inspect.stack()[1][3]}() -> building_can_not_buy is None"
    
    can_buy_img_w, can_buy_img_h = can_buy_img.shape[:-1]
    can_buy_avg_color     = get_avg_color_of_image(can_buy_img)
    can_not_buy_avg_color = get_avg_color_of_image(can_not_buy_img)

    result    = cv.matchTemplate(screenshot_img, can_buy_img, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0 and len(locations[1]) > 0:
        location  = locations[1][0], locations[0][0]
        cropped   = screenshot_img[location[1]:location[1] + can_buy_img_h, location[0]:location[0] + can_buy_img_w]
        avg_color = get_avg_color_of_image(cropped)
        if check_if_color_is_the_same(avg_color, can_buy_avg_color, max_color_delta):
            ret_val = BuildingStatus.BUILDING_PURCHASABLE
        elif check_if_color_is_the_same(avg_color, can_not_buy_avg_color, max_color_delta):
            ret_val = BuildingStatus.BUILDING_NOT_PURCHASABLE
        return [ret_val, ( location[0] + ( can_buy_img_w / 2 )), ( location[1] + ( can_buy_img_h / 2 ))]
    else:
        return [BuildingStatus.BUILDING_NOT_FOUND,0,0]

def get_avg_color_of_image(img:cv.typing.MatLike) -> [int, int, int]:
    avg_color_per_row = np.average(img, axis=0)
    avg_color         = np.average(avg_color_per_row, axis=0)
    avg_color         = np.uint8(avg_color).tolist()
    return avg_color

def check_if_color_is_the_same(color_a:[int, int, int], color_b:[int, int, int], max_delta:int):
    if abs(color_a[0] - color_b[0]) > max_delta:
        return False
    if abs(color_a[1] - color_b[1]) > max_delta:
        return False
    if abs(color_a[2] - color_b[2]) > max_delta:
        return False
    return True
