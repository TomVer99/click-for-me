import cv2 as cv

import building_detection.building_detection as building_detection

def main():

    print("Screenshot A:")
    screenshot_img = cv.imread("screenshot_a.jpg", cv.IMREAD_COLOR)

    print(*building_detection.get_array_of_building_status(screenshot_img), sep="\n")

if __name__ == "__main__":
    main()
    exit(0)
