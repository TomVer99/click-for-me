import cv2 as cv
import numpy as np
import enum

__IMAGE_PATH = "building_detection/"
__THRESHOLD = 0.9
__MAX_COLOR_DELTA = 10

class BuildingStatus(enum.Enum):
    BUILDING_NOT_FOUND = 0
    BUILDING_NOT_PURCHASABLE = 1
    BUILDING_PURCHASABLE = 2

# TODO: refactor this function so other buildings are basically copy paste with different images
def get_cursor_status(screenshot_img:cv.typing.MatLike) -> [int, int, int]:
    assert screenshot_img is not None, "get_cursor_status() -> screenshot_img is None"

    # load the can_buy image and can_not_buy image
    can_buy_img = cv.imread(__IMAGE_PATH + "cursor_buy.png", cv.IMREAD_COLOR)
    can_not_buy_img = cv.imread(__IMAGE_PATH + "cursor_no_buy.png", cv.IMREAD_COLOR)
    
    # validate the images
    assert can_buy_img is not None, "get_cursor_status() -> can_buy_img is None"
    assert can_not_buy_img is not None, "get_cursor_status() -> can_not_buy_img is None"

    # get the width and height of the images
    can_buy_img_w, can_buy_img_h = can_buy_img.shape[:-1]

    # get the average color of the images
    can_buy_avg_color = get_avg_color_of_image(can_buy_img)
    can_not_buy_avg_color = get_avg_color_of_image(can_not_buy_img)

    # find the can_buy image
    result = cv.matchTemplate(screenshot_img, can_buy_img, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= __THRESHOLD)
    if len(locations[0]) > 0 and len(locations[1]) > 0:
        location = locations[1][0], locations[0][0]
        cropped = screenshot_img[location[1]:location[1] + can_buy_img_h, location[0]:location[0] + can_buy_img_w]
        avg_color = get_avg_color_of_image(cropped)
        if check_if_color_is_the_same(avg_color, can_buy_avg_color, __MAX_COLOR_DELTA):
            ret_val = __BUILDING_PURCHASABLE
        elif check_if_color_is_the_same(avg_color, can_not_buy_avg_color, __MAX_COLOR_DELTA):
            ret_val = __BUILDING_NOT_PURCHASABLE
        print(ret_val)
        return [ret_val, ( location[0] + ( can_buy_img_w / 2 )), ( location[1] + ( can_buy_img_h / 2 ))]
    else:
        # We are assuming that the image detection does not care for the color,
        # so if we get here we can assume that the image is not on the screen
        return [__BUILDING_NOT_FOUND,0,0]

def get_avg_color_of_image(img:cv.typing.MatLike) -> [int, int, int]:
    assert img is not None, "get_avg_color_of_image() -> img is None"
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    avg_color = np.uint8(avg_color).tolist()
    return avg_color

def check_if_color_is_the_same(color_a:[int, int, int], color_b:[int, int, int], max_delta:int):
    if abs(color_a[0] - color_b[0]) > max_delta:
        return False
    if abs(color_a[1] - color_b[1]) > max_delta:
        return False
    if abs(color_a[2] - color_b[2]) > max_delta:
        return False
    return True
