import cv2 as cv
import numpy as np
import enum
import inspect
import json
import threading

__IMAGE_PATH = "building_detection/"
__THRESHOLD = 0.9
__MAX_COLOR_DELTA = 10

__HEIGHT_ITEMS = 21
__WIDTH_ITEMS = 4

class BuildingStatus(enum.Enum):
    BUILDING_NOT_FOUND = 0
    BUILDING_NOT_PURCHASABLE = 1
    BUILDING_PURCHASABLE = 2

class Building(enum.Enum):
    cursor = 0
    grandma = 1
    farm = 2
    mine = 3
    factory = 4
    bank = 5
    temple = 6
    wizard_tower = 7
    shipment = 8
    alchemy_lab = 9
    portal = 10
    time_machine = 11
    antimatter_condenser = 12
    prism = 13
    chancemaker = 14
    fractal_engine = 15
    javascript_console = 16
    idleverse = 17
    cortex_baker = 18
    you = 19

def get_array_of_building_status(screenshot_img:cv.typing.MatLike) -> [[str, BuildingStatus, int, int]]:
    ret_val = []
    for i in range(len(Building)):
        ret_val.append([Building(i).name, BuildingStatus.BUILDING_NOT_FOUND, 0, 0])
    ret_val_lock = threading.Lock()
    threads = []

    for building in Building:
        thread = threading.Thread(target=detect_building, args=(screenshot_img, building, ret_val, ret_val_lock))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return ret_val

def detect_building(screenshot_img:cv.typing.MatLike, building:Building
                    , ret_val:[[str, BuildingStatus, int, int]] = None, ret_val_lock:threading.Lock = None
                    , threshold:float = __THRESHOLD, max_color_delta:int = __MAX_COLOR_DELTA):
    assert screenshot_img  is not None, f"{inspect.stack()[1][3]}() -> screenshot_img is None"
    buildings_img = cv.imread(__IMAGE_PATH + "buildings.png", cv.IMREAD_COLOR)
    assert buildings_img is not None, f"{inspect.stack()[1][3]}() -> buildings_img is None"
    buildings_height, buildings_width, _ = buildings_img.shape
    ppc_height:int = int(buildings_height / __HEIGHT_ITEMS)
    ppc_width:int = int(buildings_width / __WIDTH_ITEMS)

    with open(__IMAGE_PATH + "buildings.json", "r") as json_file:
        json_s = json.load(json_file)
        # TODO: read more possible locations per building
        info = json_s[building.name][0]
        building_img = buildings_img[int(ppc_height * info[1]):int(ppc_height * (info[1] + 1))
                                     , int(ppc_height * info[0]):int(ppc_width * (info[0] + 1))]
        avg_color_can_buy = get_avg_color_of_image(building_img)

        result = cv.matchTemplate(screenshot_img, building_img, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        if len(locations[0]) > 0 and len(locations[1]) > 0:
            location  = locations[1][0], locations[0][0]
            cropped   = screenshot_img[location[1]:location[1] + ppc_height, location[0]:location[0] + ppc_width]
            avg_color = get_avg_color_of_image(cropped)
            
            # TODO: check color for not purchasable (decrease chance of false positive)
            if check_if_color_is_the_same(avg_color, avg_color_can_buy, max_color_delta):
                building_status = BuildingStatus.BUILDING_PURCHASABLE
            else:
                building_status = BuildingStatus.BUILDING_NOT_PURCHASABLE
            
            with ret_val_lock:
                ret_val[building.value] = [building.name, building_status, ( location[0] + ( ppc_width / 2 )), ( location[1] + ( ppc_height / 2 ))]
        else:
            with ret_val_lock:
                ret_val[building.value] = [building.name, BuildingStatus.BUILDING_NOT_FOUND, 0, 0]
    
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
